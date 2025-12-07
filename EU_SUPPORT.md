# EU Vehicle Support

This branch adds support for European vehicles to the Mitsubishi Connect integration.

## Changes Made

### Client Library (`mitsubishi_connect_client`)

1. **Region Parameter**: Added `region` parameter to `MitsubishiConnectClient.__init__()`
   - Accepts "US" (default) or "EU"
   - Automatically selects the appropriate API endpoint based on region

2. **Regional Endpoints**:
   - US: `https://us-m.aerpf.com`
   - EU: `https://eu-m.aerpf.com`

3. **Dynamic Headers**: Updated `_get_headers()` to use region-specific host values

### Home Assistant Integration (`mitsubishi_connect`)

1. **Config Flow**: Added region selection dropdown in the setup flow
   - Users can now choose between "North America (US)" and "Europe (EU)"
   - Region is stored in the config entry data

2. **Constants**: Added `CONF_REGION` constant for consistency

3. **Client Initialization**: Updated `__init__.py` to pass region to the client
   - Defaults to "US" for backward compatibility with existing installations

4. **Translations**: Updated English translations to include region field with description

## Usage

### For Users

When setting up the integration:
1. Enter your Mitsubishi Connect username and password
2. Enter your PIN
3. **Select your region** from the dropdown:
   - Choose "North America (US)" if you're in the US, Canada, or other North American regions
   - Choose "Europe (EU)" if you're in Europe

### For Developers

Using the client library directly:

```python
from mitsubishi_connect_client import MitsubishiConnectClient

# For US vehicles
us_client = MitsubishiConnectClient(
    user_name="your_username",
    password="your_password",
    region="US"  # This is the default
)

# For EU vehicles
eu_client = MitsubishiConnectClient(
    user_name="your_username",
    password="your_password",
    region="EU"
)

await eu_client.login()
vehicles = await eu_client.get_vehicles()
```

## Testing Notes

⚠️ **Important**: The EU endpoint (`https://eu-m.aerpf.com`) has not been verified yet. This implementation is based on the regional architecture patterns used by similar connected vehicle services.

### What Needs Testing

1. **EU Endpoint Verification**: Confirm that `eu-m.aerpf.com` is the correct EU endpoint
2. **OAuth Credentials**: Verify if EU uses the same OAuth client credentials as US
3. **API Compatibility**: Test that all API endpoints work identically for EU vehicles
4. **Feature Parity**: Confirm all features (climate control, lights, door lock, etc.) work for EU vehicles

### How to Test

1. Set up network monitoring (Charles Proxy, mitmproxy, or similar)
2. Install the official My Mitsubishi Connect app on an EU mobile device
3. Capture API calls during:
   - Login
   - Vehicle status retrieval
   - Remote commands (climate, lights, door lock)
4. Compare endpoints and authentication mechanisms with US implementation
5. Update the code if differences are found

## Known Limitations

1. The EU API endpoint is assumed based on common patterns but unverified
2. OAuth client credentials may differ between regions (currently using US credentials for both)
3. Some features may not be available in all EU markets
4. API rate limits and throttling may differ by region

## Next Steps

- [ ] Test with actual EU vehicles
- [ ] Verify EU endpoint URL
- [ ] Confirm OAuth credentials work for EU region
- [ ] Add region-specific error handling if needed
- [ ] Consider adding additional regions (Asia, Australia, etc.) using same pattern
- [ ] Update version numbers for release

## Backward Compatibility

Existing installations will continue to work without changes:
- Region defaults to "US" if not specified
- No migration needed for existing config entries
