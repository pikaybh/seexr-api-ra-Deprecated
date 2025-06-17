#%%
import json
import logging
import time
from copy import deepcopy
from datetime import datetime

import pandas as pd
import requests
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from tqdm import tqdm


logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('logs/eval.log'))


def evaluate_model(y_true, y_pred):
    """
    Evaluate the model's predictions against the true labels.
    
    Parameters:
    y_true (list): True labels.
    y_pred (list): Predicted labels.
    
    Returns:
    dict: A dictionary containing accuracy, F1 score, precision, and recall.
    """
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    
    return {
        'accuracy': accuracy,
        'f1_score': f1,
        'precision': precision,
        'recall': recall
    }


def save_json(data, filename='output/eval_results.json'):
    """
    Save the evaluation results to a JSON file.
    
    Parameters:
    data (dict): Evaluation results.
    filename (str): Name of the file to save the results.
    """
    with open(filename, 'w', encoding="utf-8'") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info(f"Results saved to {filename}")


def save_results(results, filename=f"res/eval_results.txt"):
    """
    Save the evaluation results to a text file.
    
    Parameters:
    results (dict): Evaluation results.
    filename (str): Name of the file to save the results.
    """
    with open(filename, 'w') as f:
        for metric, value in results.items():
            f.write(f"{metric}: {value:.4f}\n")
    logger.info(f"Results saved to {filename}")


def democracy_vote(predictions):
    """
    Perform a democracy vote on the predictions.
    
    Parameters:
    predictions (list): List of predictions from different models.
    
    Returns:
    str: The final prediction after voting.
    """
    if not predictions:
        return None
    # Count occurrences of each prediction
    counts = pd.Series(predictions).value_counts()
    # Return the most common prediction
    voted = counts.idxmax() if not counts.empty else None
    logger.debug(f"Democracy vote result: {voted} from {counts.to_dict()}")
    return voted


def main():
    eval_handler = {"output": {}, "y_true": [], "y_pred": [], "filtered": [], "results": {}}
    # Load the test dataset
    test_data = pd.read_excel("data/KRAS_SIF_OCR_합본_사고분류_250602_test.xlsx")
    
    # Prepare input and label columns
    input_columns = {
        '공정': 'process_major_category', 
        '세부공정': 'process_sub_category', 
        '설비': 'equipment', 
        '물질': 'material',
        '유해위험요인': 'hazardous_risk_factors',
    }
    label_column = '사고분류'
    y_true, y_pred = [], []

    # requests 동기 방식으로 변경
    MAX_RETRY = 3
    for idx, row in tqdm(test_data.iterrows(), total=len(test_data), desc="Processing rows (requests)"):
        payload = {
            "input": {
                **{input_columns[col]: ("" if pd.isna(row[col]) else row[col]) for col in input_columns.keys()},
                "task_description": "",
                "site_image": [],
            }
        }
        eval_handler["output"][idx] = deepcopy(payload)
        logger.debug(f"Payload for index {idx}: {payload}")
        pred = None
        for attempt in range(1, MAX_RETRY + 1):
            eval_handler["output"][idx]["attempt"] = attempt
            try:
                response = requests.post(
                    "http://snucem1.iptime.org:8000/v1/openai/gpt-4o/pi-ratings/invoke",
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"},
                    timeout=120,
                    allow_redirects=True
                )
                eval_handler["output"][idx]["status_code"] = response.status_code
                eval_handler["output"][idx]["response_text"] = response.text
                logger.debug(f"[RESPONSE {idx}] status={response.status_code}, text={response.text}")
                response.raise_for_status()
                result = response.json()
                위험성평가표 = result.get('output').get('위험성평가표')
                candidates = [위험성평가표[i].get('사고분류') for i in range(len(위험성평가표))]
                eval_handler["output"][idx]["candidates"] = candidates
                logger.debug(f"Candidates for index {idx}: {candidates}")
                pred = democracy_vote(candidates)
                eval_handler["output"][idx]["prediction"] = pred
                eval_handler["output"][idx]["true_label"] = row[label_column]
                break  # 성공 시 retry 루프 탈출
            except Exception as e:
                logger.error(f"API 호출 실패 (index={idx}, attempt={attempt}): {e}")
                if attempt == MAX_RETRY:
                    logger.error(f"최대 재시도({MAX_RETRY}) 후에도 실패. None으로 처리.")
                else:
                    time.sleep(1)  # 재시도 전 1초 대기
        y_true.append(row[label_column])
        y_pred.append(pred)
        eval_handler["y_true"] = y_true
        eval_handler["y_pred"] = y_pred
        time.sleep(0.1)  # 서버 부하 방지용 약간의 딜레이

    # Remove None or invalid predictions before evaluation
    filtered = [(t, p) for t, p in zip(y_true, y_pred) if p is not None]
    eval_handler["filtered"] = filtered
    logger.debug(f"{filtered = }, {y_pred = }")
    logger.debug(f"Filtered predictions: {len(filtered)} out of {len(y_pred)}")
    if not filtered:
        logger.error("No valid predictions to evaluate.")
        return
    y_true_filtered, y_pred_filtered = zip(*filtered)

    # Evaluate the model
    results = evaluate_model(list(y_true_filtered), list(y_pred_filtered))
    eval_handler["results"] = results
    # Print the evaluation results
    logger.info("Evaluation Results:")
    for metric, value in results.items():
        logger.info(f"{metric}: {value:.4f}")

    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_results(results, filename=f"res/{now}_eval_results.txt")
    save_json(eval_handler, filename=f"output/{now}_eval_results.json")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()