module.exports = function(config){
  var opalPath;
  if(process.env.TRAVIS){
    python_version = process.env.TRAVIS_PYTHON_VERSION;
    opalPath = '/home/travis/virtualenv/python' + python_version + '/src/opal';
  }
  else{
    opalPath = '../../opal';
  }
  var karmaDefaults = require(opalPath + '/config/karma_defaults.js');
  var karmaDir = __dirname + '/..';
  var coverageFiles = [
    __dirname + '/../referral/static/js/referral/*.js',
    __dirname + '/../referral/static/js/referral/controllers/*.js'
  ];
  var includedFiles = [
      __dirname + '/../referral/static/js/referral/*.js',
      __dirname + '/../referral/static/js/referral/controllers/*.js',
      __dirname + '/../referral/static/js/test/*.js',
  ];

  var defaultConfig = karmaDefaults(includedFiles, karmaDir, coverageFiles);
  config.set(defaultConfig);
};
