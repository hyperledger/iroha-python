//! Binary which generates classes from json schema
#![allow(clippy::unwrap_used, clippy::todo, clippy::unwrap_in_result)]

use std::env;

use iroha_schema_gen::build_schemas;
use module::Module;

mod as_py;
mod module;

fn main() -> Result<(), color_eyre::Report> {
    color_eyre::install()?;

    let args = &env::args().collect::<Vec<_>>()[1..];
    if args.is_empty() {
        return Err(color_eyre::eyre::eyre!(
            "Please provide argument with valid directory"
        ));
    }

    let module = build_schemas().into_iter().collect::<Module>();
    module.write_dir(&args[0])?;
    Ok(())
}
