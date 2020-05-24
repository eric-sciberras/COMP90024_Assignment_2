const express = require('express');
const router = express.Router();

/* GET home page. */

router.get('/', function(req, res, next) {
    res.render('index', { title: 'Dashboard', view: twitter_search});
});

module.exports = router;





/*
const request = require('request')
const url = 'http://admin:comp90024@127.0.0.1:5984/'
const db = 'test/'
const id = 'document_id'

// Create a database/collection inside CouchDB

request.put(url + db, function(err, resp, body) {
    // Add a document with an ID

    request.put({
        url: url + db + id,
        body: {message:'New Shiny Document', user: 'stefan'},
        json: true,
    }, function(err, resp, body) {

        // Read the document
        request(url + db + id, function(err, res, body) {
            console.log(body.user + ' : ' + body.message)
        })
    })
})

 */

//module.exports = request;

//not used
const view = "172.26.132.103:5984/_utils/#/database/twitter-search/_design/location/_view/mel-pos?reduce=true";

const nano = require('nano')('http://admin:instance1@172.26.132.103:5984');

// get a database
const twitter_search = nano.use('twitter-search');

//get a couchdb view (a bunch of tweets)
twitter_search.view('location', 'mel-pos').then((body) => {
    body.rows.forEach((doc) => {
        console.log(doc.value);
    });
});

//get a couchdb document (a tweet)
twitter_search.get('5703b847514f584955956d187300384a').then((body)=>{
    console.log(body);
});


/*
var responses_x_questions = require('../reports/barChart.json');
var clone = require('clone');

router.get('/', function(req, res, next) {

    var chartOptions = clone(responses_x_questions);

    var categories = ["newCat1","newCat2","newCat3","newCat4","newCat5"];

    chartOptions.xAxis[0].data = categories;
    chartOptions.series1[0].data = [10,20,30,40,50];

    res.render('index', { title: 'Express', dataa: JSON.stringify(chartOptions) });
});

 */




