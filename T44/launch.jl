using ArgParse
using JSON

function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table! s begin
        "--json-file", "-j"
            help = "set JSON parameters file path"
			arg_type = String
			default = ""
    end

    return parse_args(s)
end

function main()
    parsed_args = parse_commandline()
    println("Parsed args:")
    for (arg,val) in parsed_args
        println("  $arg  =>  $val")
    end
	jsonFile = get(parsed_args, "json-file", "")
	conf = JSON.parsefile(jsonFile)
	global parameters = get(conf, "parameters", "")
	for (arg,val) in parameters
        println("  $arg  =>  $val")
    end
	@time begin
		include("main_int.jl")
	end
end

main()