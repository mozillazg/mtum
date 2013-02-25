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

// control icon display
function displayIcon(request, hidden, display) {
  if (!document.getElementById) return false;
  if ((request.readyState == 4) && request.status == 200) {
    var icon_hidden = document.getElementById(hidden);
    var icon_display = document.getElementById(display);
    icon_hidden.className = icon_hidden.className + " hidden";
    icon_display.className = icon_display.className.replace("hidden", "");
  }
}

// ajax submit link
function ajaxLink(url_id, display) {
  var request = getHTTPObject();
  if (request) {
    var url = document.getElementById(url_id).href;
    request.open("get", url, true);
    request.onreadystatechange = function() {displayIcon(request, url_id, display);};
    request.send();
  }
}

function toggleDisplay(block, none) {
  if (!document.getElementById) return false;
  var block = document.getElementById(block);
  var none = document.getElementById(none);
  if (block.style.display != "none") {
    block.style.display = "none";
    none.style.display = "block";
  } else {
    none.style.display = "none";
    block.style.display = "block";
  }
}
