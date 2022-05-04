### Dataset original folder structure
```bash
paper_data/
├── images
│   ├── other
│   ├── test
│   └── train
└── labels
    ├── other
    ├── test
    ├── train
    ├── other.txt
    ├──	test.txt
    └── train.txt
```

### The dataset folder structure after processing

```bash
paper_data/
├── boxed_images # Processed by draw_boxes.py
│   ├── other_less_30
│   ├── test_less_30
│   └── train_less_30
├── export # processed by label_filter.py
    ├── other_inf_less_30.txt
    ├── other_inf.txt
    ├── other_less_30_table.txt
    ├── test_inf_less_30.txt
    ├── test_inf.txt
    ├── test_less_30_table.txt
    ├── train_inf_less_30.txt
    ├── train_inf.txt
    └── train_less_30_table.txt
├── images
│   ├── marks
│   ├── other
│   ├── size_less_30  # Processed by label_filter.py
│   │   ├── other
│   │   ├── test
│   │   └── train
│   ├── test
│   └── train
└── labels
    ├── other
    ├── size_less_30  # Processed by label_filter.py
    │   ├── other
    │   ├── test
    │   └── train
    ├── test
    ├── train
    ├── other.txt
    ├──	test.txt
    └── train.txt
```



