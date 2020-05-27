const express = require('express');
const router = express.Router();
const rp = require('request-promise');
const dotenv = require('dotenv').config();

const couchdb_url = process.env.COUCHDB_URL
const couchdb_port = process.env.COUCHDB_PORT
const coudchdb_username = process.env.COUCHDB_USERNAME
const couchdb_password = process.env.COUCHDB_PASSWORD

const locationSentiment = `http://${coudchdb_username}:${couchdb_password}@${couchdb_url}:${couchdb_port}/twitter_data/_design/byLocation/_view/location-sentiment?group=true`;
const dateSentiment = `http://${coudchdb_username}:${couchdb_password}@${couchdb_url}:${couchdb_port}/twitter_data/_design/byDate/_view/date-sentiment?group=true`
let location;
let avgSentiment;
let date;
let sentiment;
let tweets;

/* GET home page. */
router.get('/', function(req, res, next) {
    // average sentiment per location
    console.log(locationSentiment)
    console.log(dateSentiment)
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
            date = json.rows.map(function (e) {
                return e.key;
            });
            sentiment = json.rows.map(function (e) {
                var sum = e.value.sum;
                var count = e.value.count;
                return sum/count;
            });

            // total tweets per location
            rp(locationSentiment).then((response) => {
                var json = JSON.parse(response);

                var counts = 0;
                for(var i=0; i<json.rows.length; i++){
                    counts+=json.rows[i].value.count;
                }
                tweets = json.rows.map(function (e){
                    return e.value.count;
                });
                res.render('index', { title: 'Dashboard', location: location, avgSentiment: avgSentiment, date: date,
                    sentiment: sentiment, tweets: tweets, counts: counts});
            });
            });
        });
    });

module.exports = router;
