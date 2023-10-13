use std::io;
use std::fs;
use std::path::Path;
use std::path::PathBuf;
use glob::glob;

use minijinja::Error;
use minijinja::{Environment, context};
use std::collections::HashMap;


const BUILD_DIR: &str = "site_out";
const SRC_DIR: &str = "site_src";
const STAIC_DIR: &str = "static";


fn make_build_dir(build_dir: &Path) {
    if build_dir.exists() {
        return;
    } else {
        let _err = fs::create_dir(build_dir);
        return;
    }
}


fn collect_templates(site_src_dir: &Path) -> HashMap<String, String> {
    let mut templates = HashMap::<String, String>::new();

    for entry in glob("{site_src_dir}/*.html.jinja").expect("Failed to read glob pattern") {

        let path = entry.expect("Failed to read path");
        let temp_name = path.to_str().expect("IO Error");
        templates.insert(temp_name.to_string(), fs::read_to_string(path).expect("File read error"));
    }

    return templates;
}



