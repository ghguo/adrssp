# ADR SSP - A Content Driven Supply Side Platform
**ADR SSP** is able to:

* Receive Real Time Bidding (RTB)/Header Bidding (HB) requests with content IAB Categories and keywords;
* Pass through the IAB Categories and keywords to DSP/Adserver to match ads targeted to the IAB Categories and keywords.
* Send matched ads back to the publisher adserver.

You can find more about IAB Categoies at https://www.iab.com/guidelines/iab-quality-assurance-guidelines-qag-taxonomy/

A bid adpater sends RTB/HB requests with IAB Categories and keywords extracted from page content as First Party Data.

With Content Target Plugin, a DSP advertiser can specify which IAB Categories or keywords an ad is targeted to. When a request with the IAB Categories and keywords is received, the ad is matched and delivered.


Clone the code. Run
docker build -t ssp .

Then, run
docker run --name adrssp -d -v $PWD/app:/app -p 80:80 ssp app.py
  
