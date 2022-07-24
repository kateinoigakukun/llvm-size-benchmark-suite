BITCODE_TESTSUITE_ATTRS = {
    "target": attr.string(mandatory=True),
    "accessory_files": attr.string_list(default=[]),
    "cases": attr.label_list(default=[]),
    "ldflags": attr.string_list(default=[]),
}

BITCODE_TESTCASE_ATTRS = {
    "args": attr.string_list(default=[]),
}

BitcodeTestCaseInfo = provider(
    "A provider that contains a single test case info",
    fields = [
        "args",
    ],
)

def _bitcode_testsuite(ctx):
    output = ctx.actions.declare_file(ctx.label.name + ".manifest.json")
    ctx.actions.write(
        output,
        json.encode_indent(
            {
                "name": ctx.label.name,
                "target": ctx.attr.target,
                "accessory_files": ctx.attr.accessory_files,
                "cases": [
                    {"args": case[BitcodeTestCaseInfo].args} for case in ctx.attr.cases
                ],
                "ldflags": ctx.attr.ldflags,
            },
            indent="  ",
        ),
    )
    return [
        DefaultInfo(files = depset([output])),
    ]

bitcode_testsuite = rule(
    implementation = _bitcode_testsuite,
    attrs = BITCODE_TESTSUITE_ATTRS,
)

def _bitcode_testcase(ctx):
    return [
        BitcodeTestCaseInfo(args = ctx.attr.args),
    ]


bitcode_testcase = rule(
    implementation = _bitcode_testcase,
    attrs = BITCODE_TESTCASE_ATTRS,
)
