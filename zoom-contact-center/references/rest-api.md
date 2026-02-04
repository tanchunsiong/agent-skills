# Contact Center REST API

REST API endpoints for Contact Center data and operations.

> **Official docs:** https://developers.zoom.us/docs/api/contact-center/
> **Sample repo:** https://github.com/zoom/CRM-Sample (branch: `Contact-Center`)

## Authentication

Contact Center APIs require Admin-level OAuth with Contact Center scopes.

### Required OAuth Scopes

```
contact_center_contact:read:admin
contact_center_report:read:admin
user:read:user:admin
```

### NextAuth.js Setup

From [CRM-Sample](https://github.com/zoom/CRM-Sample/blob/Contact-Center/src/app/api/auth/%5B...nextauth%5D/route.js):

```javascript
import NextAuth from "next-auth";
import ZoomProvider from "next-auth/providers/zoom";

export const authOptions = {
  providers: [
    ZoomProvider({
      clientId: process.env.ZOOM_CLIENT_ID,
      clientSecret: process.env.ZOOM_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async jwt({ token, account, user }) {
      // Initial sign in
      if (account && user) {
        return {
          accessToken: account.access_token,
          accessTokenExpires: account.expires_at * 1000,
          refreshToken: account.refresh_token,
          user,
        };
      }

      // Return previous token if not expired
      if (token.accessTokenExpires && Date.now() < token.accessTokenExpires) {
        return token;
      }

      // Token expired, refresh it
      return refreshAccessToken(token);
    },
    async session({ session, token }) {
      session.user = token.user;
      session.accessToken = token.accessToken;
      session.error = token.error;
      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
};

async function refreshAccessToken(token) {
  try {
    const response = await fetch("https://zoom.us/oauth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: `Basic ${Buffer.from(
          `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
        ).toString("base64")}`,
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: token.refreshToken,
      }),
    });

    const refreshedTokens = await response.json();

    if (!response.ok) throw refreshedTokens;

    return {
      ...token,
      accessToken: refreshedTokens.access_token,
      accessTokenExpires: Date.now() + refreshedTokens.expires_in * 1000,
      refreshToken: refreshedTokens.refresh_token ?? token.refreshToken,
    };
  } catch (error) {
    console.error("RefreshAccessTokenError", error);
    return { ...token, error: "RefreshAccessTokenError" };
  }
}

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

## Engagements API

Get Contact Center engagement history (calls, chats).

### Endpoint

```
GET https://api.zoom.us/v2/contact_center/engagements
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `from` | string | Start date (YYYY-MM-DD) |
| `to` | string | End date (YYYY-MM-DD) |

### Example: Next.js API Route

From [CRM-Sample](https://github.com/zoom/CRM-Sample/blob/Contact-Center/src/app/api/call-history/route.js):

```javascript
import { getServerSession } from "next-auth/next";
import { authOptions } from "../auth/[...nextauth]/route";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  let from = searchParams.get("from");
  let to = searchParams.get("to");

  // Default to last 30 days
  if (!from || !to) {
    const now = new Date();
    to = now.toISOString().split("T")[0];
    from = new Date(now.setDate(now.getDate() - 30)).toISOString().split("T")[0];
  }

  try {
    const session = await getServerSession(authOptions);

    if (!session || !session.accessToken) {
      return Response.json({ error: "Not authenticated" }, { status: 401 });
    }

    let zoomUrl = "https://api.zoom.us/v2/contact_center/engagements";
    const params = new URLSearchParams();
    if (from) params.append("from", from);
    if (to) params.append("to", to);
    if (params.toString()) zoomUrl += `?${params.toString()}`;

    const response = await fetch(zoomUrl, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.accessToken}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error(`Zoom API error: ${response.status}`, errText);
      throw new Error(`Zoom API error: ${response.status} - ${errText}`);
    }

    const data = await response.json();

    // Filter for voice engagements only
    const voiceEngagements =
      data.engagements?.filter((e) =>
        e.channels?.some((c) => c.channel === "voice")
      ) || [];

    // Format response
    const formatted = voiceEngagements.map((log) => {
      const consumer = log.consumers?.[0];
      const name = consumer?.consumer_display_name || "Unknown";
      const number = consumer?.consumer_number || "";
      const formattedNumber = number
        ? `(${number.slice(-10, -7)})${number.slice(-7, -4)}-${number.slice(-4)}`
        : "";

      return {
        id: `${name}, ${formattedNumber}`,
        direction: log.direction,
        start_time: log.start_time,
        end_time: log.end_time,
        duration: log.duration,
      };
    });

    return Response.json({ interactions: formatted });
  } catch (err) {
    console.error("Zoom call logs fetch error:", err.message);
    return Response.json({ error: err.message }, { status: 500 });
  }
}
```

### Response Structure

```json
{
  "engagements": [
    {
      "engagement_id": "abc123",
      "direction": "inbound",
      "start_time": "2024-01-15T10:30:00Z",
      "end_time": "2024-01-15T10:45:00Z",
      "duration": 900,
      "channels": [
        {
          "channel": "voice",
          "channel_id": "ch_123"
        }
      ],
      "consumers": [
        {
          "consumer_display_name": "John Doe",
          "consumer_number": "+14155551234"
        }
      ]
    }
  ]
}
```

## Common API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /v2/contact_center/engagements` | List engagements (calls, chats) |
| `GET /v2/contact_center/engagements/{id}` | Get specific engagement |
| `GET /v2/contact_center/queues` | List queues |
| `GET /v2/contact_center/agents` | List agents |
| `GET /v2/contact_center/agents/{id}/status` | Get agent status |

## Error Handling

```javascript
if (!response.ok) {
  if (response.status === 401) {
    // Token expired or invalid
    return Response.json(
      { error: "API authorization failed. Please sign in again." },
      { status: 401 }
    );
  }

  const errText = await response.text();
  console.error(`Zoom API error: ${response.status}`, errText);
  throw new Error(`Zoom API error: ${response.status} - ${errText}`);
}
```

## Resources

- **API Reference:** https://developers.zoom.us/docs/api/contact-center/
- **OAuth Setup:** See [zoom-oauth skill](/zoom-oauth/SKILL.md)
- **Sample App:** https://github.com/zoom/CRM-Sample (branch: Contact-Center)
