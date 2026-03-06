import torch
from diffusion_policy.dataset.robomimic_image_dataset import RobomimicImageDataset

class MultiTaskDataset(torch.utils.data.Dataset):
    def __init__(self, task_paths, **kwargs):
        self.datasets = []
        self.task_ids = []
        for i, path in enumerate(task_paths):
            dataset = RobomimicImageDataset(dataset_path=path, **kwargs)
            self.datasets.append(dataset)
            # 각 데이터셋의 길이만큼 해당 Task ID(0, 1, 2) 저장
            self.task_ids.extend([i] * len(dataset))
            
        # 모든 데이터셋을 하나로 합친 인덱스 생성
        self.cumulative_sizes = [len(d) for d in self.datasets]
        self.total_size = sum(self.cumulative_sizes)

    def __len__(self):
        return self.total_size

    def __getitem__(self, idx):
        # 전체 인덱스를 개별 데이터셋 인덱스로 변환
        dataset_idx = 0
        curr_idx = idx
        for size in self.cumulative_sizes:
            if curr_idx < size:
                break
            curr_idx -= size
            dataset_idx += 1
            
        data = self.datasets[dataset_idx][curr_idx]
        # 모델이 인식할 수 있도록 Task ID를 추가 (One-hot 혹은 정수)
        data['task_id'] = torch.tensor([dataset_idx], dtype=torch.float32)
        return data
