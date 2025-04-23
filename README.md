# DuprlyBot
Simple Discord bot that uses DUPR's scuffed API to get player/club/match data

This project is based off of this repository: https://github.com/pkshiu/duprly

## Commands
To verify your user with your DUPR account, use one of the following command:

```
!verify Hey, have a look at my DUPR Profile https://dashboard.dupr.com/dashboard/player/1234567890
!verify https://dashboard.dupr.com/dashboard/player/1234567890
!verify 1234567890
```

Note: `1234567890` is your DUPR account's unique ID, not the DUPRID.

Check the DUPR_Share_Link.png to see where to get the link/DUPR account ID.

Check out DUPR's scuffed API: https://backend.mydupr.com/swagger-ui/

## TODO
 - Store players' data in a database to more easily manage data for future features.