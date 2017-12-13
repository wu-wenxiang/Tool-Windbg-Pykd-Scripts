"use strict"
let debugMode = false;
const scriptName = 'test';

let dbgLog = function (text) {
    host.diagnostics.debugLog(text + '\r\n');
};

let dbgVerb = function (text) {
    if (debugMode) {
        host.diagnostics.debugLog('*' + text + '*\r\n');
    }
};

let dbgError = function (text) {
    dbgLog(`!!!Error: ${text}.!!!`);
};

let exec = function (command) {
    dbgVerb(`Executing command: ${command} ...`);
    return host.namespace.Debugger.Utility.Control.ExecuteCommand(command);
};

let elementsCollectionList = null;
let cdocList = null;
let elementsList = [];
let ignoreEtagList = ['', 'NULL', 'UNKNOWN', 'ABBR', 'ACRONYM', 'BASE', 'RAW'];
let ignoreMshtmlClassNameList = ['mshtml!CCommentElement',
    'mshtml!CDefaultElement',
    'mshtml!CGeneratedElement',
    'mshtml!CRootElement'];

function enableDebug() {
    debugMode = true;
    dbgVerb('Debug mode successfully enabled!');
}

function DumpAllElements() {
    GetAllElementsFromDump();
    printJSONStr(elementsList);
}

function printJSONStr(obj) {
    let arr = JSON.stringify(obj, null, 4).split('\n');
    let printLines = '';
    exec('!mex.lo');
    for (let i = 0; i < arr.length; i++) {
        printLines += arr[i] + '\n';
        if (printLines.length > 10000) {
            dbgLog(printLines);
            printLines = '';
        }
    }
    dbgLog(printLines);
}

function GetLeakElements() {
    let startTime = new Date().getTime();
    GetAllElementsFromDump();
    GetAllCDocs();
    let leakList = [];
    let leakInvalidList = [];
    for (let i = 0; i < elementsList.length; i++) {
        let element = elementsList[i];
        if (!element.containedInMarkup && element.valid) {
            leakList.push(element);
        } else if (!element.containedInMarkup && !element.valid) {
            let found = false;
            for (let j = 0; j < leakInvalidList.length; j++) {
                if (leakInvalidList[j].name === element.mshtmlClassName) {
                    leakInvalidList[j].count++;
                    found = true;
                    break;
                }
            }
            if (!found) {
                leakInvalidList.push({
                    name: element.mshtmlClassName,
                    count: 1
                });
            }
        }
    }
    let timeTaken = Math.round((new Date().getTime() - startTime) / 1024);
    dbgLog(`GetLeakElements completes, time taken: ${timeTaken}s, ${elementsList.length} elements found in the dump.`);
    if (leakList.length) {
        dbgLog(`${leakList.length} elements were not contained by any CMarkup objects. See below for details.`)
        leakList.forEach(function (element) {
            element.dump();
        });
    } else {
        dbgLog(`No obvious leak found.`);
    }
    if (leakInvalidList.length) {
        dbgLog(`Also found some potential leak elements, see below summary.`);
        leakInvalidList.forEach(item => {
            dbgLog(`Type: ${item.name} Count: ${item.count}`);
        });
    }
}

function GetAllCDocs() {
    if (cdocList !== null) {
        return cdocList;
    }
    cdocList = [];
    let output = exec('!mex.CDocs');
    let docCheckRegExp = /^CDoc: ([0-9a-f]+)$/i;
    let markupCheckRegExp = /^ ?([0-9a-f]+) \| (\w+) +\| +([0-9a-f ]+) \| (\w+) +\| (\w+) +\| (\w+) +\| (\w*) +\| +(\w+) \| (.+)$/i;
    let currentCDocAddress = null;
    let currentCDoc = null;
    for (let line of output) {
        let matchResult = docCheckRegExp.exec(line);
        if (matchResult !== null) {
            currentCDocAddress = matchResult[1];
            cdocList.push(new CDoc(currentCDocAddress));
            currentCDoc = cdocList[cdocList.length - 1];
        } else {
            matchResult = markupCheckRegExp.exec(line);
            if (matchResult !== null) {
                let cMarkup = new CMarkup(matchResult[1], matchResult[2], matchResult[3], matchResult[4], matchResult[5], matchResult[6], matchResult[7], matchResult[8], matchResult[9]);
                currentCDoc.add(cMarkup);
                cMarkup.scanInnerElements();
            }
        }
    }
}

function GetAllElementsFromDump() {
    if (elementsCollectionList !== null) {
        return;
    }
    elementsCollectionList = [];
    elementsList = [];
    let output = exec('!mex.HtmlElements');
    let mheRegExp = /(0x[0-9a-f]+) \| (mshtml!\w+) *\| *(\d+) \|.+/i;
    for (let line of output) {
        //dbgLog('Found line: ' + line);
        let matchResult = mheRegExp.exec(line);
        if (matchResult !== null) {
            elementsCollectionList.push(new ElementsCollection(matchResult[1], matchResult[2], matchResult[3]));
        }
    }
}

class CMarkup {
    constructor(address, type, attrArray, docMode, layMode, codePageSrc, state, pinned, url) {
        this.address = address;
        this.type = type;
        this.attrArray = attrArray;
        this.docMode = docMode;
        this.layMode = layMode;
        this.codePageSrc = codePageSrc;
        this.state = state;
        this.pinned = pinned === 'True';
        this.url = url;
        this.elementList = [];
        dbgVerb(`New CMarkup found (Address = ${this.address}, Type = ${this.type}, AttrArray = ${this.attrArray}, DocMode = ${this.docMode}, LayMode = ${this.layMode}, CodePageSrc = ${this.codePageSrc}, State = ${this.state}, Pinned = ${this.pinned}, URL = ${this.url})`);
    }
    scanInnerElements() {
        let output = exec('!mex.DumpMarkup ' + this.address);
        let elementRegExp = /^\w+ +\|  [0-9a-f]+ \|  ([0-9a-f]+) \|   [0-9a-f]+ \|.+\| +[<>a-z]+$/i;
        for (let line of output) {
            let matchResult = elementRegExp.exec(line);
            if (matchResult !== null) {
                let foundElement = false;
                for (let i = 0; i < elementsList.length; i++) {
                    let cElement = elementsList[i];
                    if (cElement.address === matchResult[1]) {
                        cElement.containedInMarkup = true;
                        this.elementList.push(cElement);
                        foundElement = true;
                        break;
                    }
                }
            }
        }
    }
}

class CDoc {
    constructor(address) {
        this.address = address;
        this.CMarkupCount = 0;
        this.pinnedMarkupCount = 0;
        this.orphaedMarkupCount = 0;
        this.CMarkupList = [];
        dbgVerb(`New CDoc found, address: ${this.address}`);
    }
    add(cMarkup) {
        this.CMarkupList.push(cMarkup);
        this.CMarkupCount++;
        if (cMarkup.pinned) {
            this.pinnedMarkupCount++;
        }
        if (cMarkup.type === 'Orphaned') {
            this.orphaedMarkupCount++;
        }
    }
}

class ElementsCollection {
    constructor(address, mshtmlClassName, count) {
        this.address = address;
        this.mshtmlClassName = mshtmlClassName;
        this.count = Number(count);
        dbgVerb(`Found new elements collection (Address: ${this.address}, MshtmlClassName: ${this.mshtmlClassName}, Count: ${this.count})`);
        dbgVerb('Will go through all these elements.');
        let output = exec('!mex.DumpHtmlElements ' + this.address + ' -c ' + this.count);
        let mdheRegExp = /(0x[0-9a-f]+) \| (mshtml!\w+) \| (0x[0-9a-f]+)?/i;
        for (let line of output) {
            let matchResult = mdheRegExp.exec(line);
            if (matchResult !== null) {
                elementsList.push(new CElement(matchResult[1], matchResult[2], matchResult[3]));
            }
        }
    }
}

class CElement {
    constructor(address, mshtmlClassName, attrArray) {
        this.address = simplifyAddress(address);
        this.mshtmlClassName = mshtmlClassName;
        this.attrArray = attrArray || '';
        this.valid = true;
        this.containedInMarkup = false;
        this.attributes = [];
        let output = exec('!_mce ' + this.address);
        let etagRegExp = /ETAG +: ([a-z]+)?/i;
        let attrRegExp = /.+\|.+\|.+\|.+\| (.+) +\| (.+) \| (.+)/i;
        if (ignoreMshtmlClassNameList.indexOf(this.mshtmlClassName) > -1) {
            this.valid = false;
        }
        for (let line of output) {
            let etagResult = etagRegExp.exec(line);
            if (etagResult !== null) {
                this.etag = etagResult[1] || '';
                if (ignoreEtagList.indexOf(this.etag) > -1) {
                    this.valid = false;
                }
            }
        }
        if (this.valid) {
            output = exec('!mex.CAttrArray ' + this.attrArray);
            for (let line of output) {
                let matchResult = attrRegExp.exec(line);
                if (matchResult !== null) {
                    let propType = matchResult[1].trim();
                    let attribute = matchResult[2].trim();
                    let value = matchResult[3].trim();
                    if (attribute.length && value.length) {
                        this.attributes.push({
                            attr: attribute,
                            value: value
                        });
                    } else if (propType === 'DISPID_IHTMLELEMENT_CLASSNAME' && value.length) {
                        this.attributes.push({
                            attr: 'class',
                            value: value
                        });
                    }
                }
            }
        }
        dbgVerb(`Found new element (Address: ${this.address}, MshtmlClasName: ${this.mshtmlClassName}, ETAG: ${this.etag}, AttrArray: ${this.attrArray}, Valid: ${this.valid})`);
    }
    dump() {
        let html = 'N/A';
        if (this.valid) {
            html = `<${this.etag.toLowerCase()}`;
            for (let i = 0; i < this.attributes.length; i++) {
                html += ` ${this.attributes[i].attr}="${this.attributes[i].value}"`;
            }
            html += `></${this.etag.toLowerCase()}>`;
        }
        dbgVerb(`Address: ${this.address}, ${this.mshtmlClassName}, AttrArray: ${this.attrArray}, Valid: ${this.valid}, HTML: ${html}`);
        dbgLog(`${html} (${this.address} ${this.mshtmlClassName})`);
    }
}
function initializeScript() {
    dbgLog(`Enable debug: dx Debugger.State.Scripts.${scriptName}.Contents.enableDebug()`);
    dbgLog(`GetLeakElements: dx Debugger.State.Scripts.${scriptName}.Contents.GetLeakElements()`);
    dbgLog(`GetAllCDocs: dx Debugger.State.Scripts.${scriptName}.Contents.GetAllCDocs()`);
    dbgLog(`DumpAllElements: dx Debugger.State.Scripts.${scriptName}.Contents.DumpAllElements()`);
}

function simplifyAddress(address) {
    let regExp = /0x[0]*([0-9a-f]+)/i;
    let match = regExp.exec(address);
    if (match !== null) {
        return match[1];
    } else {
        return address;
    }
}