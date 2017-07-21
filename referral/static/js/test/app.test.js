describe('should configure our routes correctly!', function(){
    "use strict";

    var route, opalTestHelper;

    beforeEach(function(){
        module('opal.referral');
        module('opal.test');

        inject(function($injector){
            route = $injector.get('$route');
            opalTestHelper = $injector.get('opalTestHelper');
        });
    });

    it('Detail view should resolve data', function(){
        var result;
        var resolve = route.routes['/:route'].resolve;
        var recordLoader = opalTestHelper.getRecordLoader();
        var referenceDataLoader = opalTestHelper.getReferenceDataLoader();
        var referralLoader = jasmin.createSpy();
        referralLoader.and.returnValue = "as";

        expect(resolve.referral_route(referralLoader)).toBe("as");
        expect(referralLoader).toHaveBeenCalled();

        result = resolve.referencedata(referenceDataLoader);
        expect(referenceDataLoader.load()).toHaveBeenCalled();
        expect(!!result.then).toBe(true);

        result = resolve.recordFields(recordLoader);
        expect(recordLoader.load()).toHaveBeenCalled();
        expect(!!result.then).toBe(true);
    });
});
