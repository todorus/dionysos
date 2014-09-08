App = Ember.Application.create();

/*******************
      MODELS
*******************/
App.Observable = DS.Model.extend({
  label: attr("string"),
  datapoints: DS.hasMany('dataPoint')
});

App.DataPoint = DS.Model.extend({
  label: attr("string"),
  quantity: attr("string"),
  unit: attr("string"),
  datatype: attr("number"),
  observable: DS.belongsTo('observable')
});

App.Measurement = DS.Model.extend({
  value: attr(),
  time: attr("datetime"),
  datapoint: DS.belongsTo("dataPoint")
});

// datapoint = models.ForeignKey(DataPoint)
//   valueInt = models.IntegerField(null=True, blank=True)
//   valueFloat = models.FloatField(null=True, blank=True)
//   valueString = models.CharField(max_length=200,null=True, blank=True)
//   time = models.DateTimeField()

// label = models.CharField(max_length=200)
// quantity = models.CharField(max_length=200)
// unit = models.CharField(max_length=50)
// datatype = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
// observable = models.ForeignKey(Observable, null=True, blank=True)

App.Router.map(function() {
  // put your routes here
});

App.IndexRoute = Ember.Route.extend({
  model: function() {
    return ['red', 'yellow', 'blue'];
  }
});

console.log("reached app");
