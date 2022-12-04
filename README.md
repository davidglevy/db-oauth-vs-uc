# OAuth vs Unity Catalog access for ADLS

The goal of this repository is to show the difference between using OAuth to access ADLS files vs Unity Catalog (UC) with Managed Identities.

## Getting Started

Before you get started, you will need the following for OAuth and UC respectively:

### OAuth Requirements

Please record all details below, except the keys in the secret scope (you just need the key)

1. An App Registration
2. A storage account with container (LRS, with "hierarchical namespace")
3. Grant "Storage Account Contributor" to the app registration on the container for the demo.
2. A secret scope
3. The following keys in your secret scope from the app registration:
    1. directoryId
    2. applicationId
    3. keyValue
    
![This is an image](./images/secret_acls_a.png)



<img src="./images/secret_acls_a.png" />