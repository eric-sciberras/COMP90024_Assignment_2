/*
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');


var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');


//var nano = require('nano')('http://localhost:5984');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
//app.use(express.static('public'))
app.use(express.static(path.join(__dirname, 'reports')));

app.use('/', indexRouter);
app.use('/users', usersRouter);


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;

 */


const express = require('express');
const app = express();
const path = require('path');
const router = express.Router();

//var indexRouter = require('./routes/index');
//app.use('/', indexRouter);

router.get('/',function(req,res){
    res.sendFile(path.join(__dirname+'/chart.html'));

});

//add the router
app.use('/', router);
app.listen(process.env.port || 3000);

console.log('Running at Port 3000');


const nano = require('nano')('http://admin:instance1@172.26.132.103:5984');



// get a database
const twitter_search = nano.use('twitter-search');


//get a couchdb view (a bunch of tweets)
/*
twitter_search.view('location', 'locationSent').then((body) => {
    body.rows.forEach((doc) => {
        console.log(doc);
    });
});
 */


//const forbes = "https://forbes400.herokuapp.com/api/forbes400?limit=5"
const melSum = "http://admin:instance1@172.26.132.103:5984/twitter-search/_design/location/_view/locationSent?limit=5";
const melCount = "http://admin:instance1@172.26.132.103:5984/twitter-search/_design/location/_view/melCount?limit=5";
const rp = require('request-promise');

function processData(rp, melCount, melSum){
    rp(melCount).then((melcount) => {
        var json_count = JSON.parse(melcount);
        console.log(json_count);
        var count = json_count.rows[0].value;

        console.log(count);
        rp(melSum).then((melsum) => {
            /*
            console.log(melsum);
            var json_sum = JSON.parse(melsum);
            console.log(json_sum);
            var sum = json_sum.rows[0].value;
            console.log(json_sum.rows[0].key);
            console.log(sum);
            var melAvg = sum / count;
            console.log(melAvg);
            var avglist = [3, 0];
            //console.log(avglist);
            //return avglist;
            console.log(json_sum.rows);
             */
            var json_sum = JSON.parse(melsum);
            var labels = json_sum.rows.map(function (e){
                return e.key;
            });
            var values = json_sum.rows.map(function (e){
                return e.value;
            });
            console.log(labels);
            console.log(values);
        })
    })
}
module.exports = processData(rp, melCount, melSum);

/*
rp(forbes).then((response) => {
    var json = JSON.parse(response);
    var labels = json.map(function (e){
        return e.name;
    });
    var values = json.map(function (e){
        return e.finalWorth;
    });
    console.log(labels);
    console.log(values);
    //var count = json_count.rows[0].value;

    //console.log(count);

    }
)
 */
