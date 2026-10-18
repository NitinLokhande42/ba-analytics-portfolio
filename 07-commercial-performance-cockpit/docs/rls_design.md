# Row-Level Security Design

| Role | Filter | Margin pages |
|---|---|---|
| Executive | None (all data) | Yes |
| Finance | None | Yes |
| Regional head | `DIM_GEOGRAPHY[region] IN user's regions` | No |
| Territory manager / KAM | `DIM_GEOGRAPHY[territory] IN user's territories` | No |

**Implementation:** a `SEC_USER_GEO` mapping table in Snowflake (user email → region/territory), loaded into the model;
dynamic DAX rule `[user_email] = USERPRINCIPALNAME()` on the bridge table. Object-level security hides margin columns
for non-finance roles. Mapping maintained by sales ops; changes approved via ticket.

**Testing:** "View as role" for each role plus 10 named test users; export test; negative tests (user with no mapping sees nothing).
