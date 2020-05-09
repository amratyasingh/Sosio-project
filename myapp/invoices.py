import sys
import chilkat

rest = chilkat.CkRest()
# 4F5EA85EE9EC426CB05F3DB7F0C73FEF
# dEByy8g7rliGWbHwkicST1SZ8XtG4fBg1TRKqsX951llM359
# x30amratyasingh
oauth1 = chilkat.CkOAuth1()
oauth1.put_ConsumerKey("OAUTH1_CONSUMER_KEY")
oauth1.put_ConsumerSecret("OAUTH1_CONSUMER_SECRET")
oauth1.put_Token("OAUTH1_TOKEN")
oauth1.put_TokenSecret("OAUTH1_TOKEN_SECRET")
oauth1.put_SignatureMethod("RSA-SHA1")
rsaKey = chilkat.CkPrivateKey()
#  Insert code here to load the RSA private key...
#  ...
#  then call SetRsaKey to provide the RSA key to the OAuth1 class.
success = oauth1.SetRsaKey(rsaKey)
rest.SetAuthOAuth1(oauth1,False)

success = rest.Connect("api.xero.com",443,True,True)
if (success != True):
    print(rest.lastErrorText())
    sys.exit()

#  The following code creates the JSON request body.
#  The JSON created by this code is shown below.
jsonReq = chilkat.CkJsonObject()
jsonReq.UpdateString("Type","ACCREC")
jsonReq.UpdateString("Contact.ContactID","eaa28f49-6028-4b6e-bb12-d8f6278073fc")
jsonReq.UpdateString("Date","/Date(1518685950940+0000)/")
jsonReq.UpdateString("DueDate","/Date(1518685950940+0000)/")
jsonReq.UpdateString("DateString","2009-05-27T00:00:00")
jsonReq.UpdateString("DueDateString","2009-06-06T00:00:00")
jsonReq.UpdateString("LineAmountTypes","Exclusive")
jsonReq.UpdateString("LineItems[0].Description","Consulting services as agreed (20% off standard rate)")
jsonReq.UpdateString("LineItems[0].Quantity","10")
jsonReq.UpdateString("LineItems[0].UnitAmount","100.00")
jsonReq.UpdateString("LineItems[0].AccountCode","200")
jsonReq.UpdateString("LineItems[0].DiscountRate","20")

sbReq = chilkat.CkStringBuilder()
jsonReq.EmitSb(sbReq)

rest.AddHeader("Content-Type","application/json")

sbResponse = chilkat.CkStringBuilder()
success = rest.FullRequestSb("POST","/api.xro/2.0/Invoices",sbReq,sbResponse)
if (success != True):
    print(rest.lastErrorText())
    sys.exit()

if (rest.get_ResponseStatusCode() != 200):
    print("Received error response code: " + str(rest.get_ResponseStatusCode()))
    print("Response body:")
    print(sbResponse.getAsString())
    sys.exit()

print("Example Completed.")