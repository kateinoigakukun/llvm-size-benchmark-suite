BITCODE_TESTCASE_ATTRS = {
    "target": attr.string(mandatory=True),
    "accessory_files": attr.string_list(default=[]),
    "args": attr.string_list(default=[]),
}

def _bitcode_testcase(ctx):
    output = ctx.actions.declare_file(ctx.label.name + ".manifest.json")
    ctx.actions.write(
        output,
        json.encode_indent(
            {
                "name": ctx.label.name,
                "target": ctx.attr.target,
                "accessory_files": ctx.attr.accessory_files,
                "args": ctx.attr.args,
            },
            indent="  ",
        ),
    )
    return [
        DefaultInfo(files = depset([output])),
    ]

bitcode_testcase = rule(
    implementation = _bitcode_testcase,
    attrs = BITCODE_TESTCASE_ATTRS,
)
