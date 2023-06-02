1. User interacts with webApp to Generate xapp deep link QR Code
2. User interacts with xumm to open scan tab
3. xumm interacts with webApp to Scan xapp deep link QR code
4. xumm interacts with xummAPI to Get xapp deep link data
5. xummAPI interacts with xummDeeplinkBackend to call deeplink backend to generate payload
6. xummDeeplinkBackend interacts with xumm to redirect to xumm with `payload ['next']['always']`
7. xumm interacts with User to show signing screen
8. User interacts with xumm to sign transaction