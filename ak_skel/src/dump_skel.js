import { spine } from './spine-webgl.js';   // 3.8
import { skel2Json } from "./skel2Json.js"; // 3.5
import * as fs from 'fs';

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
            console.log(a);
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
    return skelData.animations;
}

//console.log(parseAnimations("TextAsset/char_017_huang_as#1.skel.txt"));
//console.log(parseAnimations("TextAsset/char_300_phenxi.skel.txt"));

//var files = fs.readdirSync("TextAsset");
var files = fs.readdirSync("Text_test");
var result = {};
var repeat_count = {};

files.forEach(f => {
    var charId = f.split(".")[0];

    try {
        if (!repeat_count[charId]) {
            repeat_count[charId] = 0;
            result[charId] = {};
        }
        repeat_count[charId] += 1;
        console.log(`${f} -> ${charId} - instance #${repeat_count[charId]}`);
        Object.assign(result[charId], parseAnimations(`Text_test/${f}`));
    } catch (e) {
        console.log(e);
        console.log("------");
    }
});

// 声明cache变量，便于匹配是否有循环引用的情况
// https://cloud.tencent.com/developer/article/1653935
var cache = [];
var str = JSON.stringify(result, function(key, value) {
    if (typeof value === 'object' && value !== null) {
        if (cache.indexOf(value) !== -1) {
            // 移除
            return;
        }
        // 收集所有的值
        cache.push(value);
    }
    return value;
}, 2);
fs.writeFileSync("out.json", str);
console.log("-- done. ");
