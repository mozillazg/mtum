// 用于更新 window.onload 事件
function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    }
  }
}

// 检测 XMLHttpRequest 对象是否可用
// 当可用时返回一个 XMLHttpRequest 对象
function getHTTPObject() {
  if (typeof XMLHttpRequest == "undefined") {
    XMLHttpRequest = function() {
      try { return new ActiveXObject("Msxml2.XMLHTTP.6.0");
      } catch (e) {}
      try { return new ActiveXObject("Msxml2.XMLHTTP.3.0");
      } catch (e) {}
      return false;
    }
  }
  return new XMLHttpRequest();
}

// display unlike icon
function displayUnlike(request, like) {
  if (!document.getElementById) return false;
  if ((request.readyState == 4) && request.status == 200) {
    var like_icon = document.getElementById("like");
    var unlike_icon = document.getElementById("unlike");
    if (like == "like") {
      like_icon.className = like_icon.className + " hidden";
      unlike_icon.className = unlike_icon.className.replace("hidden", "");
    } else {
      like_icon.className = like_icon.className.replace("hidden", "");
      unlike_icon.className = unlike_icon.className + " hidden";
    }
  }
}

// ajax submit like
function ajaxLike(id) {
  var request = getHTTPObject();
  if (request) {
    var url = document.getElementById(id).href;
    request.open("get", url, true);
    request.onreadystatechange = function() {displayUnlike(request, id);};
    request.send();
  }
}

// add click event on like link
function clickEvent() {
  if (!document.getElementById) return false;
  document.getElementById("like").onclick = function() {
    ajaxLike("like");
    return false;
  }
  document.getElementById("unlike").onclick = function() {
    ajaxLike("unlike");
    return false;
  }
}

addLoadEvent(clickEvent);
