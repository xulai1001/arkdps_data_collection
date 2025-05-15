import { spine } from './spine-webgl.js';   // 3.8
import { skel2Json } from "./skel2Json.js"; // 3.5
import * as fs from 'fs';
import * as path from 'path';

//console.log(spine);

var defaultRegion = {
    u: 0,
    v: 0,
    u2: 0,
    v2: 0,
    width: 0,
    height: 0,
    rotate: false,
    offsetX: 0,
    offsetY: 0,
    originalWidth: 0,
    originalHeight: 0
};

var AtlasAttachmentLoader = (function () {
    function AtlasAttachmentLoader() {
        this.atlas = null;
    }

    AtlasAttachmentLoader.prototype.newRegionAttachment = function (skin, name, path) {
        var region = defaultRegion;
        region.renderObject = region;
        var attachment = new spine.RegionAttachment(name);
        attachment.setRegion(region);
        return attachment;
    };
    AtlasAttachmentLoader.prototype.newMeshAttachment = function (skin, name, path) {
        var region = defaultRegion;
        region.renderObject = region;
        var attachment = new spine.MeshAttachment(name);
        attachment.region = region;
        return attachment;
    };
    AtlasAttachmentLoader.prototype.newBoundingBoxAttachment = function (skin, name) {
        return new spine.BoundingBoxAttachment(name);
    };
    AtlasAttachmentLoader.prototype.newPathAttachment = function (skin, name) {
        return new spine.PathAttachment(name);
    };
    AtlasAttachmentLoader.prototype.newPointAttachment = function (skin, name) {
        return new spine.PointAttachment(name);
    };
    AtlasAttachmentLoader.prototype.newClippingAttachment = function (skin, name) {
        return new spine.ClippingAttachment(name);
    };
    return AtlasAttachmentLoader;
}());

function toFrame(x) { return Math.round(x * 3000) / 100; }

function parseAnimations(filename) {
    var skel = new spine.SkeletonBinary(new AtlasAttachmentLoader);
    var skelFile = fs.readFileSync(filename);
    var skelData = skel.readSkeletonData(skelFile);
    var anims = {version: skelData.version};
    
    if (skelData.version.startsWith("3.5")) {
        // old version skel, reload
        skelData = skel2Json(skelFile);
        Object.keys(skelData.animations).forEach(a => {
            if (skelData.animations[a].events) {
                anims[a] = { duration: toFrame(skelData.animations[a].duration) };
                skelData.animations[a].events.forEach(ev => {
                    anims[a][ev.name] = toFrame(ev.time);
                });
            } else {
                anims[a] = toFrame(skelData.animations[a].duration);
            }
        });
    } else {
        skelData.animations.forEach(a => {
            anims[a.name] = toFrame(a.duration);
            a.timelines.forEach(tl => {
                if (tl.events) {
                    anims[a.name] = { duration: toFrame(a.duration) };
                    tl.events.forEach(ev => {
                        anims[a.name][ev.data.name] = toFrame(ev.time);
                    });
                }
            });
        });
    }
    return anims;
}

function findSkelFiles(startPath) {
    let results = [];
    
    function scanDirectory(directory) {
        const items = fs.readdirSync(directory);
        
        items.forEach(item => {
            const fullPath = path.join(directory, item);
            const stat = fs.statSync(fullPath);
            
            if (stat.isDirectory()) {
                scanDirectory(fullPath); // 递归扫描子目录
            } else if (path.extname(item) === '.skel') {
                results.push(fullPath); // 收集.skel文件
            }
        });
    }
    
    scanDirectory(startPath);
    return results;
}

//console.log(parseAnimations("TextAsset/char_017_huang_as#1.skel.txt"));
//console.log(parseAnimations("TextAsset/char_300_phenxi.skel.txt"));

//var files = fs.readdirSync("TextAsset");
var files = findSkelFiles("../spine/BattleFront");
//var files = fs.readdirSync("Text_test");
var result = {};
var repeat_count = {};

files.forEach(f => {
    console.log(f);
    
    var charId = f.split("\\").slice(-1)[0].split(".")[0];

    try {
        if (!repeat_count[charId]) {
            repeat_count[charId] = 0;
            result[charId] = {};
        }
        repeat_count[charId] += 1;
        console.log(`${charId} - instance #${repeat_count[charId]}`);
        Object.assign(result[charId], parseAnimations(f));
    } catch (e) {
        console.log(e);
        console.log("------");
    }
});

fs.writeFileSync("dps_anim.json", JSON.stringify(result, null, 2));
//fs.writeFileSync("dps_anim.txt", JSON.stringify(result, null, 2));
console.log("-- done. ");
