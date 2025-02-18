import random
import os
from langcodes import Language
import argparse

def parse_args():
    parser = argparse.ArgumentParser("", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-w', "--workspace", type=str, default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'), help="Workspace dir")
    parser.add_argument('-tn', "--test-name", type=str, required=True, help="wmt22/wmt21/...")
    parser.add_argument('-m', "--model-name", type=str, required=True, help="model name")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument('-s', "--src", type=str, required=True, help='source lang')
    parser.add_argument('-t', "--tgt", type=str, required=True, help='target lang')
    return parser.parse_args()

def main(args):
    workspace = args.workspace
    data_dir=os.path.join(workspace, "data")
    raw_dir=os.path.join(data_dir, "raw")
    format_dir=os.path.join(data_dir, "format")
    test_name = args.test_name
    model_name = args.model_name
    seed = args.seed
    src = args.src
    tgt = args.tgt
    src_full = Language.make(language=src).display_name()
    tgt_full = Language.make(language=tgt).display_name()
    model_out_dir = os.path.join(workspace, "output", model_name)
    output_dir = os.path.join(format_dir, "with-knowledge", model_name)

    # seed random
    random.seed(seed)

    # read files
    with open(os.path.join(raw_dir, f"{test_name}.{src}-{tgt}.{src}")) as test_src_f, \
        open(os.path.join(model_out_dir, f"{test_name}.{src}-{tgt}.{src}.5-shot.ask-demo.trans")) as demo_f:

        test_src_lines = [l.strip() for l in test_src_f.readlines()]
        demo_lines = [l.strip() for l in demo_f.readlines()]

        out_file_path = os.path.join(output_dir, f"{test_name}.{src}-{tgt}.{src}.demo.{seed}-seed")
        demos = []

        with open(out_file_path, 'w') as out_f:
            for id, (src_line, demo_line) in enumerate(zip(test_src_lines, demo_lines)):
                all_items = demos + [(src_line, None, demo_line)]
                prompt_lst = []
                for it in all_items:
                    it_src, it_tgt, it_demo = it
                    s = f"Related {src_full}-{tgt_full} sentence pairs: {it_demo}\n\n" + \
                    f"Instruction: Given the above knowledge, translate the following {src_full} text into {tgt_full}.\n" + \
                    f"{src_full}: {it_src}\n" + \
                    (f"{tgt_full}: {it_tgt}" if it_tgt else f"{tgt_full}:")
                    prompt_lst.append(s)
                prompt = "\n\n".join(prompt_lst)
                out_f.write(
                    f"{id:04}\n"
                    f"{prompt}\n\n\n"
                )

if __name__ == "__main__":
    args = parse_args()
    main(args)