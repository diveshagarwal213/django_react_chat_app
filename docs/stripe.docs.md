# local testing

```bash
stripe listen --forward-to localhost:5000/api/payments/webhook/
```
```bash
stripe trigger --help
```
```bash
stripe trigger {trigger_event}
```

# Events descriptions

## customer.subscription.deleted
 