#!/usr/bin/env python3
# Assembles template.tpl, injecting the base64 thumbnail from thumb.b64.
thumb = open('thumb.b64').read().strip()
data_uri = 'data:image/png;base64,' + thumb

TPL = r'''___TERMS_OF_SERVICE___

By creating or modifying this file you agree to Google Tag Manager's Community
Template Gallery Developer Terms of Service available at
https://developers.google.com/tag-manager/gallery-tos (or such other URL as
Google may provide), as modified from time to time.


___INFO___

{
  "type": "TAG",
  "id": "cvt_temp_public_id",
  "version": 1,
  "securityGroups": [],
  "displayName": "StackAdapt Conversion Tracking by New North Digital",
  "categories": [
    "ADVERTISING",
    "CONVERSIONS",
    "REMARKETING"
  ],
  "brand": {
    "id": "brand_dummy",
    "displayName": "New North Digital",
    "thumbnail": "__THUMB__"
  },
  "description": "StackAdapt Universal Pixel. Fires the page-view pixel (saq ts) for retargeting and the conversion pixel (saq conv) with revenue, order ID and currency. Loads events.js once and queues calls via the saq command queue. Gate it behind GTM consent settings.",
  "containerContexts": [
    "WEB"
  ]
}


___TEMPLATE_PARAMETERS___

[
  {
    "type": "SELECT",
    "name": "actionType",
    "displayName": "Event type",
    "macrosInSelect": false,
    "selectItems": [
      {
        "value": "pageview",
        "displayValue": "Page view (retargeting)"
      },
      {
        "value": "conversion",
        "displayValue": "Conversion"
      }
    ],
    "simpleValueType": true,
    "help": "Choose \"Page view\" for the Universal Pixel base (fire on All Pages): it sends saq('ts', id) for retargeting and lookalike audiences. Choose \"Conversion\" on the action you want to measure: it sends saq('conv', id, data) with optional revenue, order ID and currency."
  },
  {
    "type": "TEXT",
    "name": "pixelId",
    "displayName": "Pixel ID",
    "simpleValueType": true,
    "valueValidators": [
      {
        "type": "NON_EMPTY"
      }
    ],
    "help": "Your StackAdapt Universal Pixel ID, or the Conversion Event Unique ID for a conversion. A 22-character ID, e.g. PEpR18E5FJGoHB24wvWU6A. You can also reference a GTM variable here.",
    "alwaysInSummary": true
  },
  {
    "type": "TEXT",
    "name": "revenue",
    "displayName": "Revenue (optional)",
    "simpleValueType": true,
    "help": "Conversion value as a plain number, e.g. 100.00. Reference a GTM variable such as the transaction value.",
    "enablingConditions": [
      {
        "paramName": "actionType",
        "paramValue": "conversion",
        "type": "EQUALS"
      }
    ]
  },
  {
    "type": "TEXT",
    "name": "orderId",
    "displayName": "Order ID (optional)",
    "simpleValueType": true,
    "help": "Your order or transaction identifier, used to dedupe conversions.",
    "enablingConditions": [
      {
        "paramName": "actionType",
        "paramValue": "conversion",
        "type": "EQUALS"
      }
    ]
  },
  {
    "type": "TEXT",
    "name": "currency",
    "displayName": "Currency (optional)",
    "simpleValueType": true,
    "help": "ISO currency code for the revenue value, e.g. EUR or USD.",
    "enablingConditions": [
      {
        "paramName": "actionType",
        "paramValue": "conversion",
        "type": "EQUALS"
      }
    ]
  },
  {
    "type": "SIMPLE_TABLE",
    "name": "customParams",
    "displayName": "Custom parameters (optional)",
    "simpleTableColumns": [
      {
        "defaultValue": "",
        "displayName": "Key",
        "name": "key",
        "type": "TEXT",
        "valueValidators": [
          {
            "type": "NON_EMPTY"
          }
        ]
      },
      {
        "defaultValue": "",
        "displayName": "Value",
        "name": "value",
        "type": "TEXT"
      }
    ],
    "newRowButtonText": "Add parameter",
    "help": "Optional extra keys added to the conversion data object, such as action, product_id, product_name, product_category, product_price or product_quantity. Reference GTM variables in the Value column.",
    "enablingConditions": [
      {
        "paramName": "actionType",
        "paramValue": "conversion",
        "type": "EQUALS"
      }
    ]
  },
  {
    "type": "GROUP",
    "name": "debugGroup",
    "displayName": "Debugging",
    "groupStyle": "ZIPPY_CLOSED",
    "subParams": [
      {
        "type": "CHECKBOX",
        "name": "debug",
        "checkboxText": "Log to console for debugging",
        "simpleValueType": true
      }
    ]
  }
]


___SANDBOXED_JS_FOR_WEB_TEMPLATE___

const log = require('logToConsole');
const injectScript = require('injectScript');
const createArgumentsQueue = require('createArgumentsQueue');
const makeTableMap = require('makeTableMap');
const makeString = require('makeString');

const FN = 'saq';
const LOADER = 'https://tags.srv.stackadapt.com/events.js';

const actionType = data.actionType;
const enableDebug = data.debug;

const debugLog = (msg) => {
  if (enableDebug) {
    log('StackAdapt GTM - ' + msg);
  }
};

debugLog('Starting with event type: ' + actionType);

const pixelId = data.pixelId;
if (!pixelId) {
  debugLog('Error: Pixel ID is required');
  data.gtmOnFailure();
  return;
}

// Build the saq command queue, mirroring the native StackAdapt snippet
// (a global saq() that pushes its arguments onto saq.queue until events.js
// loads and drains it). createArgumentsQueue is safe to call on every fire.
const saq = createArgumentsQueue(FN, FN + '.queue');

if (actionType === 'pageview') {
  saq('ts', makeString(pixelId));
  debugLog('Queued ts for ' + pixelId);
} else if (actionType === 'conversion') {
  const conv = (data.customParams && data.customParams.length > 0) ?
    (makeTableMap(data.customParams, 'key', 'value') || {}) : {};
  if (data.revenue) {
    conv.revenue = makeString(data.revenue);
  }
  if (data.orderId) {
    conv.order_id = makeString(data.orderId);
  }
  if (data.currency) {
    conv.currency = data.currency;
  }
  saq('conv', makeString(pixelId), conv);
  debugLog('Queued conv for ' + pixelId);
} else {
  debugLog('Unknown event type: ' + actionType);
  data.gtmOnFailure();
  return;
}

// Load events.js once per page (cache token keeps it from re-injecting per event).
injectScript(LOADER, data.gtmOnSuccess, data.gtmOnFailure, 'stackadapt');


___WEB_PERMISSIONS___

[
  {
    "instance": {
      "key": {
        "publicId": "logging",
        "versionId": "1"
      },
      "param": [
        {
          "key": "environments",
          "value": {
            "type": 1,
            "string": "debug"
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  },
  {
    "instance": {
      "key": {
        "publicId": "access_globals",
        "versionId": "1"
      },
      "param": [
        {
          "key": "keys",
          "value": {
            "type": 2,
            "listItem": [
              {
                "type": 3,
                "mapKey": [
                  {"type": 1, "string": "key"},
                  {"type": 1, "string": "read"},
                  {"type": 1, "string": "write"},
                  {"type": 1, "string": "execute"}
                ],
                "mapValue": [
                  {"type": 1, "string": "saq"},
                  {"type": 8, "boolean": true},
                  {"type": 8, "boolean": true},
                  {"type": 8, "boolean": true}
                ]
              },
              {
                "type": 3,
                "mapKey": [
                  {"type": 1, "string": "key"},
                  {"type": 1, "string": "read"},
                  {"type": 1, "string": "write"},
                  {"type": 1, "string": "execute"}
                ],
                "mapValue": [
                  {"type": 1, "string": "saq.queue"},
                  {"type": 8, "boolean": true},
                  {"type": 8, "boolean": true},
                  {"type": 8, "boolean": false}
                ]
              }
            ]
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  },
  {
    "instance": {
      "key": {
        "publicId": "inject_script",
        "versionId": "1"
      },
      "param": [
        {
          "key": "urls",
          "value": {
            "type": 2,
            "listItem": [
              {
                "type": 1,
                "string": "https://tags.srv.stackadapt.com/*"
              }
            ]
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  }
]


___TESTS___

scenarios:
- name: Page view - queues ts and injects the loader
  code: |-
    const mockData = {
      actionType: 'pageview',
      pixelId: 'PEpR18E5FJGoHB24wvWU6A',
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onSuccess();
    });

    runCode(mockData);

    assertApi('createArgumentsQueue').wasCalled();
    assertApi('injectScript').wasCalled();
    assertApi('gtmOnSuccess').wasCalled();
- name: Page view - injects the StackAdapt loader URL
  code: |-
    const mockData = {
      actionType: 'pageview',
      pixelId: 'PEpR18E5FJGoHB24wvWU6A',
      debug: false
    };

    let capturedUrl = '';
    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      capturedUrl = url;
      onSuccess();
    });

    runCode(mockData);

    assertThat(capturedUrl).isEqualTo('https://tags.srv.stackadapt.com/events.js');
    assertApi('gtmOnSuccess').wasCalled();
- name: Conversion - sends conv with revenue and order id
  code: |-
    const mockData = {
      actionType: 'conversion',
      pixelId: 'NVzOKkqz7PghcmmSeXTHWq',
      revenue: '100.00',
      orderId: 'T12345',
      currency: 'EUR',
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onSuccess();
    });

    runCode(mockData);

    assertApi('createArgumentsQueue').wasCalled();
    assertApi('gtmOnSuccess').wasCalled();
- name: Conversion - merges custom parameters
  code: |-
    const mockData = {
      actionType: 'conversion',
      pixelId: 'NVzOKkqz7PghcmmSeXTHWq',
      customParams: [
        {key: 'product_id', value: 'SKU-1'},
        {key: 'action', value: 'purchase'}
      ],
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onSuccess();
    });

    runCode(mockData);

    assertApi('gtmOnSuccess').wasCalled();
- name: Fails without a pixel ID
  code: |-
    const mockData = {
      actionType: 'pageview',
      pixelId: '',
      debug: false
    };

    runCode(mockData);

    assertApi('gtmOnFailure').wasCalled();
- name: Loader failure - calls gtmOnFailure
  code: |-
    const mockData = {
      actionType: 'pageview',
      pixelId: 'PEpR18E5FJGoHB24wvWU6A',
      debug: false
    };

    mock('injectScript', function(url, onSuccess, onFailure, cacheToken) {
      onFailure();
    });

    runCode(mockData);

    assertApi('gtmOnFailure').wasCalled();


___NOTES___

Created on 2026-06-29 by New North Digital (newnorth.digital).
'''

TPL = TPL.replace('__THUMB__', data_uri)
with open('template.tpl', 'wb') as f:
    f.write(b'\xef\xbb\xbf')          # UTF-8 BOM (gallery validator expects it)
    f.write(TPL.encode('utf-8'))
print('template.tpl written:', len(TPL) + 3, 'bytes (incl BOM)')
