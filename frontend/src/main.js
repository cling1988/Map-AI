import './app.css';
import { Loader } from "@googlemaps/js-api-loader";
// import { info } from "./data";
import { getDistanceFromLatLonInKm } from "./utils";

const body = /*html*/`
<section class="mx-auto max-w-3xl px-4 sm:px-6 xl:max-w-5xl xl:px-0">
  <h1 class="text-2xl">Query</h1>
  <div class="flex justify-center space-x-1 my-4">
    <input id="queryText" type="text" placeholder="Enter your query" class="input input-bordered w-full" maxlength="1000"/>
    <button id="searchQuery" class="btn">Query</button>
    <span  id="searchLoading" class="loading loading-spinner loading-lg invisible"></span>
  </div>
  <div class="flex justify-center space-x-1 my-4">
    <label class="form-control w-full">
      <div class="label">
        <span class="label-text">Answer</span>
      </div>
      <textarea id="answerText" class="textarea textarea-bordered h-24" placeholder="answer" disabled></textarea>
    </label>
  </div>
  <div class="divider"></div> 
  <main class="mb-auto">
    <div class="flow-root my-2">  
      <div class="float-left">
        <h1 class="text-2xl">MAP</h1>
      </div>
      <div class="float-right">
        <select id="selectOutlet" class="select select-bordered w-full max-w-xs">
          <option disabled selected>Select Outlet</option>
        </select>
      </div>
    </div>
    <div class="min-h-screen w-full card shadow-xl">
      <div id="map" class="min-h-screen"></div>
    </div> 
  </main>
</section>
`

document.querySelector("#app").innerHTML = body;
const baseHostURL = import.meta.env.VITE_BASE_HOST ? import.meta.env.VITE_BASE_HOST : ""
// Query setup
document.getElementById("searchQuery").addEventListener("click", getQuery);
async function getQuery() {
  const queryText = document.getElementById("queryText");
  const answerText = document.getElementById("answerText");
  const searchQuery = document.getElementById("searchQuery");
  const searchLoading = document.getElementById("searchLoading");
  if (queryText.value) {
    searchQuery.classList.add("invisible");
    searchLoading.classList.remove("invisible");
    
    const bodyData = {"question":queryText.value};
    const response = await fetch(`${baseHostURL}/api/query`,
      { method: 'POST',
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      },
       body: JSON.stringify(bodyData) });
    let data = await response.json();
    console.log(data);

    answerText.value  = `Q:${data["input"]}\r\nA:${data["output"]}`;
    queryText.value = "";
    searchQuery.classList.remove("invisible");
    searchLoading.classList.add("invisible");
  }

}


// Map setup
let centerPosition = null;
const markerArray = [];
let infoWindow = null;
let content = "";
let selectedId = null;
let selectedMarker = null;
let map, circle;
const loader = createMapLoader();


const info = await getInfo();
createDropdown();
await createMap(loader)
await createMarker(loader, info);

async function getInfo() {
  const response = await fetch(`${baseHostURL}/api/outlets`);
  let info = await response.json();
  centerPosition = { lat: info[0].latitude, lng: info[0].longitude }
  content = `<article class="text-wrap"><h3>${info[0].name}</h3><p>${info[0].address}</p><p>${info[0].operation_hour}</p></article>`;
  selectedId = info[0].id;
  return info
}

function createDropdown() {
  const selectOutlet = document.getElementById("selectOutlet");
  info.forEach((data) => {
    selectOutlet.options.add(new Option(data.name, data.id));

  });
  selectOutlet.onchange = (event) => {
    let selectId = event.target.value;
    let result = info.filter(obj => {
      return obj.id === parseInt(selectId);
    });
    centerPosition = { lat: result[0].latitude, lng: result[0].longitude };
    selectedId = result[0].id;
    createMarker(loader, info);
  };
}

function createMapLoader() {
  return new Loader({
    apiKey: import.meta.env.VITE_GOOGLE_API_TOKEN,
    version: "weekly",
  });
}

async function createMap(loader) {
  const { Map, InfoWindow, Circle } = await loader.importLibrary("maps");
  infoWindow = new InfoWindow();
  const mapOptions = {
    center: centerPosition,
    zoom: 13,
    mapId: `${Map.DEMO_MAP_ID}`
  }

  map = new Map(document.getElementById("map"), mapOptions);
  circle = new Circle({
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.35,
    map,
    center: centerPosition,
    radius: 5000,
  });
}

function centerMap() {
  map.panTo(centerPosition);
  circle.setCenter(centerPosition);
  infoWindow.close();
  infoWindow.setContent(content);
  infoWindow.open(map, selectedMarker);
}


async function createMarker(loader) {
  const { AdvancedMarkerElement } = await loader.importLibrary("marker");

  while (markerArray.length > 0) {
    let mark = markerArray.pop();
    mark.map = null;
  }
  info.forEach((data) => {
    const result = getDistanceFromLatLonInKm(centerPosition.lat, centerPosition.lng, data.latitude, data.longitude);
    if (result > 5) {
      return
    }

    const marker = new AdvancedMarkerElement({
      map,
      position: { lat: data.latitude, lng: data.longitude },
      title: data.name
    });
    marker.addListener("click", () => {
      centerPosition = marker.position;
      selectedId = data.id;
      createMarker(loader);
    });

    if (selectedId === data.id) {
      selectedMarker = marker;
      content = `<article class="text-wrap"><h3>${data.name}</h3><p>${data.address}</p><p>${data.operation_hour}</p></article>`;
    }
    markerArray.push(marker);
  });
  centerMap();
}


