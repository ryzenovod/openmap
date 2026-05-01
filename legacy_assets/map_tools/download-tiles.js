//https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
const { exec } = require('child_process');
const fs = require('fs');

function lon2tile(lon, zoom) { return (Math.floor((lon + 180) / 360 * Math.pow(2, zoom))); }
function lat2tile(lat, zoom) { return (Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, zoom))); }

function download (url, output) {
    // compose the wget command
    var wget = 'wget -P ' + output + ' ' + url;
    // excute wget using child_process' exec function

    exec(wget);
   
}  //download('https://c.tile.openstreetmap.org/1/1/1.png', 'wget_node.png');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getTilesPizza(zoom, top_tile, left_tile, bottom_tile, right_tile, overwrite) {
    const servers = ['a', 'b', 'c'];
    for (let htile = left_tile; htile <= right_tile; htile++) {
        const dirpath = `tiles/${zoom}/${htile}/`;
        fs.mkdirSync(dirpath, { recursive: true });
        for (let vtile = top_tile; vtile <= bottom_tile; vtile++) {
            const path = `tiles/${zoom}/${htile}/${vtile}.png`;
            if (fs.existsSync(path) && !overwrite) {
                const stats = fs.statSync(path);
                if (stats["size"] > 0) continue;
                console.log('zero size ' + path);
            }
            const s = servers[(Math.random() * 3) | 0];
            const url = `https://${s}.tile.openstreetmap.org/${zoom}/${htile}/${vtile}.png`;
            const percenth = Math.floor(((htile - left_tile) / (right_tile - left_tile)) * 100);
            const percentv = Math.floor(((vtile - top_tile) / (bottom_tile - top_tile)) * 100);
            console.log(url + '\t\t\t' + percenth + '%\t' + percentv + '%');
            await sleep(250);
            download(url, dirpath);
        }
    }
}

const north_edge = 48.5;
const west_edge = 130.3;
const south_edge = 42.2;
const east_edge = 139.2;


async function getTilesCake(min_zoom, max_zoom, north_edge, west_edge, south_edge, east_edge, overwrite = false) {
    for (let zoom = min_zoom; zoom <= max_zoom; zoom++) {
        const top_tile = lat2tile(north_edge, zoom);
        const left_tile = lon2tile(west_edge, zoom);
        const bottom_tile = lat2tile(south_edge, zoom);
        const right_tile = lon2tile(east_edge, zoom);
        //https://c.tile.openstreetmap.org/{zoom}/{left}/{top}.png

        await getTilesPizza(zoom, top_tile, left_tile, bottom_tile, right_tile, overwrite);
    }
}
getTilesCake(0, 15, north_edge, west_edge, south_edge, east_edge);
