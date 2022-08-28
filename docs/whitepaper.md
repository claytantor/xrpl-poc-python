# xInvoice and xURL Protocols

**IMPORTANT: THIS IS A WORK IN PROGRESS. IT IS INTENDED TO BE PRESENTED TO THE XRP COMMUNITY FOR REVIEW**

## Introduction
Making a payment is a common task for any business, and making payment easy for users is a key goal for any payment network. The key challenge is to make the payment process as easy as possible for all users in the ecosystem both on both sides of the transaction. xInvoice and xURL are two protocols intended for the XRP payment ecosystem that aim to make the payment process as easy as possible for all users by abstracting and separating the activities of creating payment requests and automating the generation of payment requests using a backend.

## Use Cases

### Scan To Pay
"Scan to Pay" is a use case for the xURL protocol. It is a way for users to automate the creation of an xInvoice using a backend. This allows the seller to create a QR code that can be scanned by the buyer to create a payment request at the time of purchase. 

![Scan To Pay Cupcake Vendor](./images/usecase_1.png)

Merchants can have a new customer driven payment experience with little to no POS overhead because it is payer-driven, and can be verified on the payer wallet with little or no POS interaction.

### On Demand Fulfillment
"On Demand Fulfillment"  is a way for merchants to create a payment request that can be fulfilled by the buyer at the time of scan, and can be converted from fiat at the time of payment. These can be used over and over by the buyer to receive goods and trigger backend fulfillment. This is ideal for B2B restocking or rental use cases.

![On Demand Fulfillment](./images/usecase_2.png)

### Asymmetric Payment Technologies
"Asymmetric Payment Technologies" is a way for merchants to create a payment request in a printed form that can be fulfilled by the buyer at the time of scan, and doesn't require that the seller have a smart device to accept payment. Since the buyer is initiating payment, and that payment can be verified on the buyer's wallet, this can be used when the seller may not have direct access to a mobile device or computer.

![On Demand Fulfillment](./images/usecase_3.png)


# xInvoice
xInvoice is simply put a payment request made by a wallet that asks the payer for a specific amount of XRP to be sent to a specific address, and is signed by the requesting wallet so it can be guaranteed as coming from the correct requesting address. The payment request is a JSON object that contains the following fields:

```

```


