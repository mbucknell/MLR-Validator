
from .base_cross_field_validator import BaseCrossFieldValidator

class CrossFieldErrorValidator(BaseCrossFieldValidator):

    def _validate_reciprocal_dependency(self, keys, error_key):
        '''
        If not all values null or all non null an error will be
        added to self._errors using error_key as the object key
        :param list of str keys:
        :param str error_key: key to be used if an error is found
        '''
        if self._any_fields_in_document(keys):
            values = [self.merged_document.get(key, '').strip() for key in keys]
            all_null = [value for value in values if value != '' ] == []
            all_not_null = [value for value in values if value == ''] == []
            if not (all_null or all_not_null):
                self._errors[error_key] = \
                    ['The following fields must all be empty or all must not be empty: {0}'.format(', '.join(keys))]

    def _validate_use_code(self, primaryKey, secondaryKey, tertiaryKey):
        keys = [primaryKey, secondaryKey, tertiaryKey]
        if self._any_fields_in_document(keys):
            primary, secondary, tertiary = [self.merged_document.get(key, '').strip() for key in keys]

            if tertiary and (not primary or not secondary):
                self._errors[tertiaryKey] =['Primary and secondary must be non null if tertiary is non null']
            elif secondary and not primary:
                self._errors[secondaryKey] = ['Primary must be non null if secondary is non null']
            elif (primary and secondary and tertiary) and ((primary == secondary) or (primary == tertiary) or (secondary == tertiary)):
                self._errors[primaryKey] = ['Primary, secondary, and tertiary fields must be unique']
            elif (primary and secondary and not tertiary) and (primary == secondary):
                self._errors[primaryKey] = ['Primary and secondary must be unique']

    def _validate_site_dates(self):
        keys = ['firstConstructionDate', 'siteEstablishmentDate']
        if self._any_fields_in_document(keys):
            construction_date, inventory_date = [self.merged_document.get(key, '').strip() for key in keys]
            if (construction_date and inventory_date) and (construction_date > inventory_date):
                self._errors['site_dates'] = ["firstConstructionDate cannot be more recent than siteEstablishmentDate"]

    def _validate_depths(self):
        keys = ['holeDepth', 'wellDepth']
        if self._any_fields_in_document(keys):
            try:
                hole_depth, well_depth = [float(self.merged_document.get(key, '').strip()) for key in keys]
            except ValueError:
                pass
            else:
                if (hole_depth and well_depth) and (well_depth > hole_depth):
                    self._errors['depths'] = ["wellDepth cannot be greater than holeDepth"]

    def _validate_drainage_area(self):
        keys = ['drainageArea', 'contributingDrainageArea']
        if self._any_fields_in_document(keys):
            drainage_area, contributing_drainage_area = [self.merged_document.get(key, '').strip() for key in keys]
            if contributing_drainage_area and not drainage_area:
                self._errors['contributingDrainageArea'] = ['Can not have contributingDrainageArea without drainageArea']
            else:
                try:
                    if (drainage_area and contributing_drainage_area) and float(contributing_drainage_area) > float(drainage_area):
                        self._errors['drainageArea'] = ['contributingDrainageArea can not be larger than drainageArea']
                except ValueError:
                    pass


    def validate(self, document, existing_document):
        '''
        After validate is called the error property will reflect the errors generated by the last call to validate
        :param dict document:
        :param dict existing_document:
        :return: boolean
        '''

        super().validate(document, existing_document)
        self._validate_reciprocal_dependency([
            'latitude',
            'longitude',
            'coordinateAccuracyCode',
            'coordinateDatumCode',
            'coordinateMethodCode'
        ], 'location')
        self._validate_reciprocal_dependency([
            'altitude',
            'altitudeDatumCode',
            'altitudeMethodCode',
            'altitudeAccuracyValue'
            ], 'altitude')
        self._validate_use_code('primaryUseOfSite', 'secondaryUseOfSite', 'tertiaryUseOfSiteCode')
        self._validate_use_code('primaryUseOfWaterCode', 'secondaryUseOfWaterCode', 'tertiaryUseOfWaterCode')
        self._validate_site_dates()
        self._validate_depths()
        self._validate_drainage_area()

        return self._errors == {}

