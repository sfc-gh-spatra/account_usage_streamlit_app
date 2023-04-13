# Introduction

The aim of the app is to create an automated process to create customer account_usage views within snowhouse.It has several use cases which can help the Solutions Architect/Consultant on a day to day basis 

## Components

- Reference Table Name : account_usage_view_mapping
- Python Stored Procedure : account_usage_view_deploy
- Stage Name :account_usage_sproc (Directory table enabled)
- Streamlit App : Account Usage App (Snowhouse)

## Usage

All the objects are created in the central schema called UTIL under TEMP database.

You need to make an entry to the account_usage_view_mapping table with the view defination (Not required when all the view are there)

The Streamlit App will need the following input :

- Customer Name : 
- Customer Deployment : (Can be eleminated later)
- Replication Group : This one is not required but calculated internally
- Schema Name: This is for now all the scehma within temp database (Can be changed later where user can provide a specific name)


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## Roadmap

- No need to add customer deployment

- Performance Improvment


## Appendix

Currently Schema switch is not working as expected.

