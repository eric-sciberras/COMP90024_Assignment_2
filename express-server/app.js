app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
//app.use(express.static('public'))


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


/*
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
*/

//const nano = require('nano')('http://admin:instance1@172.26.132.103:5984');

// get a database
//const twitter_search = nano.use('twitter-search');


//get a couchdb view (a bunch of tweets)
/*
twitter_search.view('location', 'locationSent').then((body) => {
    body.rows.forEach((doc) => {
        console.log(doc);
    });
});
 */
//const forbes = "https://forbes400.herokuapp.com/api/forbes400?limit=5"

/*
function processData(rp, melCount, melSum){
    rp(melCount).then((melcount) => {
        var json_count = JSON.parse(melcount);
        console.log(json_count);
        var count = json_count.rows[0].value;

        console.log(count);
        rp(melSum).then((melsum) => {
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
 */
