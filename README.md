# Jenkills - A toolkit against Jenkins for offensive and defensive analysis.
```

░░░░░██╗███████╗███╗░░██╗██╗░░██╗██╗██╗░░░░░██╗░░░░░░██████╗
░░░░░██║██╔════╝████╗░██║██║░██╔╝██║██║░░░░░██║░░░░░██╔════╝
░░░░░██║█████╗░░██╔██╗██║█████═╝░██║██║░░░░░██║░░░░░╚█████╗░
██╗░░██║██╔══╝░░██║╚████║██╔═██╗░██║██║░░░░░██║░░░░░░╚═══██╗
╚█████╔╝███████╗██║░╚███║██║░╚██╗██║███████╗███████╗██████╔╝
░╚════╝░╚══════╝╚═╝░░╚══╝╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚═════╝░
```
This toolkit consists of multiple automation scripts,pipelines scripts,groovy scripts,techniques which can be used for both offensive and defensive purpose against Jenkins.

These are some PoC scripts I wrote while working on this project : https://github.com/dibsy/Recipies-Of-A-Jenkins-Hacker 
### Recon

- Get information from /jenkins/api
- Check for access for various rest endpoints
- Jenkins versions
- Find Jenkins Controllers with Admin Privileges
- Find Jobs with Configure Privileges
- Find Jobs with Replay Privileges 

### Dumping

- Credential Identifiers
- Build Logs
- Artifacts
- Configuration

### Audit

- Script Console 
