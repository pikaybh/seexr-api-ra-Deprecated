// const baseUrl = 'http://dev.launchpack.co.kr:1111/';
// const chatUrl = 'http://13.115.179.147:91';

Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
}

Array.prototype.move = function(from, to) {
  this.splice(to, 0, this.splice(from, 1)[0]);
};


function find(item, key, val) {
  function findVal(item) {
    return item[key] === val;
  }
  if(item === undefined) return undefined;
  return item.find(findVal);
}

function findArray(item, key, val) {

  function findVal(itm) {
    return itm[key] === val;
  }

  return item.filter(findVal);
}

function cloneItem(obj) {
  if (obj === null || typeof(obj) !== 'object')
    return obj;
  var copy = obj.constructor();
  for (var attr in obj) {
    if (obj.hasOwnProperty(attr)) {
      copy[attr] = cloneItem(obj[attr]);
    }
  }

  return copy;
}

// 전화번호 자동 하이픈
function autoHyphenPhone(str){
  str = str.replace(/[^0-9]/g, '');
  var tmp = '';

  if(str.substr(0,2) === '02') {
    if (str.length < 3) {
      return str;
    } else if (str.length < 6) {
      tmp += str.substr(0, 2);
      tmp += '-';
      tmp += str.substr(2);
      return tmp;
    } else if (str.length < 10) {
      tmp += str.substr(0, 2);
      tmp += '-';
      tmp += str.substr(2, 3);
      tmp += '-';
      tmp += str.substr(5);
      return tmp;
    } else {
      tmp += str.substr(0, 2);
      tmp += '-';
      tmp += str.substr(2, 4);
      tmp += '-';
      tmp += str.substr(6);
      return tmp;
    }
  }
  else {
    if (str.length < 4) {
      return str;
    } else if (str.length < 7) {
      tmp += str.substr(0, 3);
      tmp += '-';
      tmp += str.substr(3);
      return tmp;
    } else if (str.length < 11) {
      tmp += str.substr(0, 3);
      tmp += '-';
      tmp += str.substr(3, 3);
      tmp += '-';
      tmp += str.substr(6);
      return tmp;
    } else {
      tmp += str.substr(0, 3);
      tmp += '-';
      tmp += str.substr(3, 4);
      tmp += '-';
      tmp += str.substr(7);
      return tmp;
    }
  }
  return str;
}

// 사업자번호 자동 하이픈
function autoHyphenBiz(str){
  str = str.replace(/[^0-9]/g, '');
  var tmp = '';

  if (str.length < 4) {
    return str;
  } else if (str.length < 6) {
    tmp += str.substr(0, 3);
    tmp += '-';
    tmp += str.substr(3);
    return tmp;
  } else if (str.length < 10) {
    tmp += str.substr(0, 3);
    tmp += '-';
    tmp += str.substr(3, 2);
    tmp += '-';
    tmp += str.substr(5);
    return tmp;
  } else {
    tmp += str.substr(0, 3);
    tmp += '-';
    tmp += str.substr(3, 2);
    tmp += '-';
    tmp += str.substr(5, 5);
    return tmp;
  }

  return str;
}
