const express = require('express');
const router = express.Router();
const rp = require('request-promise');

//const locSent = "http://admin:instance1@172.26.132.103:5984/twitter-search/_design/location/_view/locationSent?limit=5";
const locationSentiment = "http://admin:instance1@172.26.132.103:5984/twitter_data/_design/byLocation/_view/location-sentiment?group=true";
const dateSentiment = "http://admin:instance1@172.26.132.103:5984/twitter_data/_design/byDate/_view/date-sentiment?limit=100"
const melSentiment = "http://admin:instance1@172.26.132.103:5984/twitter_data/_design/byLocation/_view/mel-sentiment";
let location;
let avgSentiment;
let date;
let sentiment;

//const axios = require('axios');
//const requestUrl = "http://172.26.132.103:5984/twitter-search/_design/location/_view/locationSent"

/* GET home page. */
router.get('/', function(req, res, next) {

    // average sentiment per location
    rp(locationSentiment).then((response) => {
        var json = JSON.parse(response);
        location = json.rows.map(function (e){
            return e.key;
        });
        avgSentiment = json.rows.map(function (e){
            var sum = e.value.sum;
            var count = e.value.count;
            return sum/count;
        });

        // historical sentiment
        rp(dateSentiment).then((response) => {
            var json = JSON.parse(response);
            date = json.rows.map(function (e){
                return e.key;
            });
            sentiment = json.rows.map(function (e){
                return e.value;
            });

            res.render('index', { title: 'Dashboard', location: location, avgSentiment: avgSentiment, date: date,
                sentiment: sentiment});
        });
    });
});

module.exports = router;

/*
//get a couchdb document (a tweet)
twitter_search.get('5703b847514f584955956d187300384a').then((body)=>{
    console.log(body);
});

const nano = require('nano')('http://admin:instance1@172.26.132.103:5984');

// get a database
const twitter_search = nano.use('twitter-search');

//get a couchdb view (a bunch of tweets)
twitter_search.view('location', 'mel-pos').then((body) => {
    body.rows.forEach((doc) => {
        console.log(doc.value);
    });
});
*/
