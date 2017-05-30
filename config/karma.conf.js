module.exports = function(config){
  var opalPath = process.env.OPAL_LOCATION;
  var karmaDefaults = require(opalPath + '/config/karma_defaults.js');
  var baseDir = __dirname + '/..';
  var coverageFiles = [
    __dirname + '/../referral/static/js/referral/*.js',
    __dirname + '/../referral/static/js/referral/controllers/*.js'
  ];
  var includedFiles = [
      __dirname + '/../referral/static/js/referral/*.js',
      __dirname + '/../referral/static/js/referral/controllers/*.js',
      __dirname + '/../referral/static/js/test/*.js',
  ];

  var defaultConfig = karmaDefaults(includedFiles, baseDir, coverageFiles);
  config.set(defaultConfig);
};
