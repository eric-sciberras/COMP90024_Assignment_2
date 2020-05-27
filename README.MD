# COMP90024 Assignment 2

## Directory Structure

```
├── assignment-2
│   ├── assignment-2.sh
│   ├── assignment-2.yaml
│   ├── files 
│   │   ├── dashboard
│   │   └── twitter-harvester
│   ├── hosts
│   ├── host_vars
│   │   ├── couchdb.yaml
│   │   ├── nectar-couchdb-twitter-harvester.yaml
│   │   ├── nectar-dashboard.yaml
│   │   ├── twitter-harvester copy.yaml
│   │   └── twitter-harvester.yaml
│   ├── openrc.sh
│   └── roles
│       ├── build-instances
│       │   ├── openstack-common
│       │   ├── openstack-instance
│       │   ├── openstack-security-group
│       │   ├── openstack-volume
│       │   └── openstack-volume-snapshot
│       ├── post-run-configure
│       │   └── couchdb
│       └── run-services
│           ├── common
│           ├── couchdb
│           ├── dashboard
│           └── twitter-harvester
└── README.MD
```

`files/`: Holds the twitter harvester and dashboard code
`host_vars/`: Holds parameters for the playbook
`assignment-2.sh`: Runs the ansible playbook 

## Running the Ansible Playbook

1. Go to Melbourne Research cloud and retreive a copy of `.openrc.sh` for your project, and replace it with the current `.openrc.sh`.
2. In the `host_vars/twitter-harvester.yaml` file modify `twitter_credentials` object to add your API keys like so
```
twitter_credentials:
  access_token:
    - <access_token_1>
    - <access_token_2>
    - <access_token_3>
  access_token_secret:
    - <access_token_secret_1>
    - <access_token_secret_2>
    - <access_token_secret_3>
  consumer_key:
    - <consumer_key_1>
    - <consumer_key_2> 
    - <consumer_key_3>
  consumer_secret:
    - <consumer_secret_1>
    - <consumer_secret_2>
    - <consumer_secret_3>
```
3. For slack integration, In the same file add a slack webhook url in the `slack_webhook_url` field.
4. in the `assignment-2` folder run 
   ```
   ./assignment-2.sh
   ```