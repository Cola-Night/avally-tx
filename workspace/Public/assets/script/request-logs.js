
/** [init] App-Context (Global App) */
function initApplication() {
  window.App = {
    RequestLogs: {
      Records: [],
      Total: 0,
    },
    View: {},
  };
}

/** (Promise/fetch) */
function updateRequestLogs() {
  return new Promise((resolve,reject) => {
    // Send HTTP-Request (Promise)
    let req = fetch('/api/v1/request-logs/records.json');

    // Request failed
    req.catch((error)=>{
      reject(error);
    });

    // Request success
    req.then((response) => {

      // JSON-decode
      let decode = response.json();

      // Decode failed
      decode.catch((error)=>{
        reject(error);
      });

      // Decode success
      decode.then((data)=>{
        renderRequestLogs(data);
        resolve(data);
      });

    });
  });
}

/** Render-HTML */
function renderRequestLogs(data = {}) {

  // Update App-Context
  App.RequestLogs = data;

  // 
  const find = "#request-logs";
  const wrap = document.querySelector(find);

  // Find table elements
  const table = wrap.querySelector("table");
  const tbody = table.querySelector("[data-body=records]");

  console.log("table",{table,tbody});

}

/* document ready */
document.addEventListener("DOMContentLoaded",()=>{

  // [init]
  initApplication();

  // experiment
  updateRequestLogs().then((data)=>{
    console.log("response",data);
  });

});