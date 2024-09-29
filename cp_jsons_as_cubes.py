import sys
import os
import json


def make_smaller_sim_dump(filename_sim_dump, filename_small_sim_dump):
    buffer = ''
    break_word = ', \"photon_register\"'
    buff_limit = len(break_word)
    with open(filename_sim_dump, 'r') as input:
        with open(filename_small_sim_dump, 'w') as output:
            while True:
                char = input.read(1)
                if not char: 
                    break
                buffer += char
                if len(buffer) > buff_limit:
                    output.write(buffer[0])
                    buffer = buffer[1:]
                if buffer == break_word:
                    output.write('}')
                    break


def load_json_pack(dirpath):
    filename_sim_dump = "sim_dump.json"
    filename_result_env = "resultEnv.json"
    filename_light_source = "DefaultLightSource.json"

    results_path = os.path.join(dirpath, 'resultRecords')
    light_source_path = os.path.join(dirpath, 'lightSources')

    filename_sim_dump = os.path.join(results_path, filename_sim_dump)
    filename_result_env = os.path.join(results_path, filename_result_env)
    filename_light_source = os.path.join(light_source_path, filename_light_source)
    filename_small_sim_dump = os.path.join(results_path, 'small_sim_dump.json')

    print('load sim dump - start')
    make_smaller_sim_dump(filename_sim_dump, filename_small_sim_dump)
    file_sim_dump = open(filename_small_sim_dump, 'r')
    sim_dump = json.load(file_sim_dump)
    file_sim_dump.close()
    print('load sim dump - done')

    print('load result env - start')
    file_result_env = open(filename_result_env, 'r')
    result_env = json.load(file_result_env)
    file_result_env.close()
    print('load result env - done')

    print('load light source - start')
    file_light_source = open(filename_light_source, 'r')
    light_source = json.load(file_light_source)
    file_light_source.close()
    print('load light source - done')

    return sim_dump, result_env, light_source


def make_cube_dict(sim_dump, result_env, light_source):
    ls_photons = light_source['photon_limit']
    print('make cube - start')
    print(ls_photons)
    cube_dict = {
                "n_photons": light_source['photon_limit'],
                "overflow": sim_dump['escaped_photons_weight'],
                "bins_per_1_cm": sim_dump['config']['bins_per_1_cm'],
                "cube": result_env['resultEnv'],
                "mu_a": sim_dump['config']['tissue_properties']['4'],
                "name": f'mati_{ ls_photons }mln_cube',
                "photon_weight": 1.0,
                "normalized_already": False
            }
    print('make cube - done')
    return cube_dict



input_dirs = ['mati-sim 2-layers',
              'mati-sim 3-layers',
              'mati-sim my_params 10k g {0, 0.5, 0.9, 1}',
              'mati-sim my_params 10k-100mln',
              'mati-sim org_params 10k-10mln',
              'mati-sim veins']
full_input_dirs = input_dirs.copy()
str_experiment = 'experiments_done'
full_input_dirs[2] = os.path.join(full_input_dirs[2], str_experiment)
full_input_dirs[3] = os.path.join(full_input_dirs[3], str_experiment)
full_input_dirs[4] = os.path.join(full_input_dirs[4], str_experiment)
output_dirname = "CUBES"

# full_input_dirs = full_input_dirs[3:]
# input_dirs = input_dirs[3:]



if output_dirname in os.listdir():
    print("{} already exists!".format(output_dirname))
else:
    os.mkdir(output_dirname)


for i in range(len(full_input_dirs)):

    # walk - returns (dirpath, dirnames, filenames)
    for (dirpath, found_dirs, filenames) in os.walk(full_input_dirs[i]):
        if "resultRecords" in found_dirs:
            print(dirpath)
            sim_dump, result_env, light_source = load_json_pack(dirpath)
            cube_dict = make_cube_dict(sim_dump, result_env, light_source)

            cube_json_name = os.path.join(input_dirs[i], dirpath, 'cube.json').replace('/', '_').replace('\\', '_')
            save_path = os.path.join(output_dirname, input_dirs[i], cube_json_name)

            print('saving cube to file - start')
            with open(save_path, "w") as f:
                json.dump(cube_dict, f)
            print('saving cube to file - done')

    print("{} DONE".format(__file__))



# DONE