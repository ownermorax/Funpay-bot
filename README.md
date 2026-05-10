# FunPay Gift Bot

A bot for automatically sending notifications to buyers on FunPay after an order is paid.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![FunPayBotEngine](https://img.shields.io/badge/FunPayBotEngine-latest-green.svg)
![Asyncio](https://img.shields.io/badge/Asyncio-3.7+-orange.svg)

## About the Project

FunPay Gift Bot is an asynchronous bot for the FunPay platform that automatically tracks new paid orders and sends buyers a notification about the gift being sent, extracting the account name from the order title.

### Features

- Real-time automatic tracking of new paid orders
- Processing of existing paid orders on startup
- Extraction of account name from the order title
- Automatic detection of chat_id for sending messages
- Sending personalized messages mentioning the buyer's account
- Asynchronous architecture for high performance
- Logging of all actions to the console
- Resilience to network and API errors
