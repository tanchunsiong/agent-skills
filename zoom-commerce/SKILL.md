---
name: zoom-commerce
description: |
  Zoom Commerce and monetization integration guide. Covers selling and distributing Zoom Apps
  through the Zoom App Marketplace, implementing in-app purchases, subscription management,
  and revenue tracking. Use when building paid Zoom Apps or managing app monetization.
---

# Zoom Commerce & Monetization

Build revenue-generating Zoom Apps with in-app purchases, subscriptions, and marketplace distribution.

## Overview

Zoom Commerce enables developers to:
- Sell Zoom Apps through the Marketplace
- Implement in-app purchases and subscriptions
- Manage entitlements and access control
- Track revenue and sales analytics
- Handle billing and invoicing through Zoom

## Key Features

| Feature | Description |
|---------|-------------|
| **Marketplace Distribution** | List and sell apps in Zoom Marketplace |
| **In-App Purchases** | Sell features, add-ons, or upgrades |
| **Subscriptions** | Offer recurring billing plans |
| **Entitlements** | Manage user access to paid features |
| **Revenue Share** | 85% developer / 15% Zoom split |
| **Global Payments** | Zoom handles international billing |

## Choose Your Integration

| I want to... | Use this |
|--------------|----------|
| Sell my app on Marketplace | **Marketplace Listing** |
| Add in-app purchases | **Commerce API** |
| Offer subscription plans | **Subscription API** |
| Check user entitlements | **Entitlements API** |
| Track sales and revenue | **Analytics Dashboard** |
| Handle purchase webhooks | **zoom-webhooks** |

## Monetization Models

| Model | Description | Best For |
|-------|-------------|----------|
| **Free** | No charge, optional premium | User acquisition |
| **Freemium** | Free tier + paid upgrades | Conversion funnel |
| **Subscription** | Monthly/yearly recurring | Ongoing value |
| **One-time Purchase** | Single payment | Perpetual features |
| **Usage-based** | Pay per use/API call | Variable consumption |

## Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/commerce/entitlements` | List user entitlements |
| POST | `/commerce/entitlements/check` | Check specific entitlement |
| GET | `/commerce/subscriptions` | List subscriptions |
| GET | `/commerce/subscriptions/{subId}` | Get subscription details |
| POST | `/commerce/subscriptions/{subId}/cancel` | Cancel subscription |
| GET | `/commerce/purchases` | List purchases |
| GET | `/commerce/products` | List available products |

## Common Operations

### Check User Entitlement

```javascript
// Check if user has access to a paid feature
const response = await fetch(
  'https://api.zoom.us/v2/commerce/entitlements/check',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: 'user_abc',
      product_id: 'premium_feature'
    })
  }
);

const { entitled } = await response.json();
if (entitled) {
  // Grant access to premium feature
}
```

### List User Subscriptions

```javascript
const response = await fetch(
  'https://api.zoom.us/v2/commerce/subscriptions?user_id=user_abc',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const { subscriptions } = await response.json();
// subscriptions[].plan_id, subscriptions[].status
```

### Initiate Purchase Flow

```javascript
// In your Zoom App (client-side)
const zoomSdk = window.zoomSdk;

// Open Zoom's purchase modal
await zoomSdk.openPurchaseFlow({
  product_id: 'premium_plan',
  success_url: 'https://yourapp.com/purchase/success',
  cancel_url: 'https://yourapp.com/purchase/cancel'
});
```

## Setting Up Monetization

### 1. Configure Products in Marketplace

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/) -> Manage -> Your App
2. Navigate to **Monetization** tab
3. Add products/plans:
   - Product name and description
   - Pricing (monthly/yearly/one-time)
   - Feature entitlements
4. Submit for review

### 2. Implement Entitlement Checks

```javascript
// Middleware to check paid access
async function requirePremium(req, res, next) {
  const entitled = await checkEntitlement(req.user.id, 'premium');
  if (!entitled) {
    return res.status(403).json({ 
      error: 'Premium subscription required',
      upgrade_url: '/upgrade'
    });
  }
  next();
}
```

### 3. Handle Purchase Webhooks

```javascript
// Webhook handler for purchase events
app.post('/webhooks/zoom', (req, res) => {
  const { event, payload } = req.body;
  
  switch (event) {
    case 'app.entitlement_granted':
      // User purchased - grant access
      grantAccess(payload.user_id, payload.product_id);
      break;
    case 'app.entitlement_revoked':
      // Subscription cancelled/expired - revoke access
      revokeAccess(payload.user_id, payload.product_id);
      break;
    case 'app.subscription_renewed':
      // Subscription renewed - extend access
      extendAccess(payload.user_id, payload.subscription_id);
      break;
  }
  
  res.sendStatus(200);
});
```

## Pricing Best Practices

| Practice | Description |
|----------|-------------|
| **Tiered Plans** | Offer multiple price points (Basic, Pro, Enterprise) |
| **Annual Discount** | 15-20% off for yearly billing |
| **Free Trial** | 7-14 day trial to drive conversions |
| **Seat-based** | Per-user pricing for team features |
| **Usage Limits** | Free tier with usage caps |

## Revenue Share

| Party | Share |
|-------|-------|
| Developer | 85% |
| Zoom | 15% |

- Zoom handles all payment processing
- Payouts via Stripe Connect or bank transfer
- Monthly payout schedule
- Minimum $100 threshold

## Prerequisites

1. **Published Zoom App** - App must be live on Marketplace
2. **Stripe Connect Account** - For receiving payouts
3. **Tax Information** - Required for payouts
4. **Monetization Agreement** - Accept Zoom's monetization terms

## Common Use Cases

| Use Case | Description | Model |
|----------|-------------|-------|
| **Pro Features** | Advanced functionality locked | Freemium |
| **Team Plans** | Multi-user access | Subscription |
| **API Access** | Programmatic access tier | Usage-based |
| **White Label** | Remove branding | One-time |
| **Support Tiers** | Priority support | Subscription |

## Webhooks

Commerce-related webhook events:

| Event | Trigger |
|-------|---------|
| `app.entitlement_granted` | User purchased/subscribed |
| `app.entitlement_revoked` | Access revoked/expired |
| `app.subscription_renewed` | Subscription renewed |
| `app.subscription_cancelled` | User cancelled |
| `app.trial_started` | Free trial began |
| `app.trial_ended` | Free trial expired |

See **zoom-webhooks** skill for webhook setup.

## Resources

- **Monetization Guide**: https://developers.zoom.us/docs/distribute/monetization/
- **Marketplace Distribution**: https://developers.zoom.us/docs/distribute/
- **Revenue Dashboard**: https://marketplace.zoom.us/develop/analytics
- **Payout Setup**: https://marketplace.zoom.us/develop/payouts
