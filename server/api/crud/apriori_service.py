import pandas as pd
from sqlalchemy.orm import Session
from apyori import apriori, load_transactions

from ..schemas import AssociationRuleRow, StatisticsRow

from ..crud.file_service import _get_file_path, get_file_by_id


def get_frequency_table_from_file(db: Session, file_id: int):
  file = get_file_by_id(db, file_id)
  path = _get_file_path(file)
  transactions: pd.DataFrame = pd.read_csv(path, header=None)
  data = transactions.values.reshape(-1)

  table = pd.DataFrame(data)
  table[1] = 0
  table = table.groupby(0, as_index=False)[1].count()
  table[2] = table[1] / table[1].sum()

  table = table.sort_values(by=[1], ascending=False)

  table = table.rename(columns={0: 'Item', 1: 'Frequency', 2: 'Relative'})

  records = table.to_dict('records')

  def to_row(s): return StatisticsRow(
      item=s['Item'], frequency=s['Frequency'], relative=s['Relative'])
  records = list(map(to_row, records))

  return records


def get_rules_from_file(db: Session, file_id: int, min_support, min_confidence, min_lift):
    file = get_file_by_id(db, file_id)
    file_path = _get_file_path(file)

    content = pd.read_csv(file_path, header=None)

    transactions = content.stack().groupby(level=0).apply(list).tolist()
    rules = apriori(
        transactions=transactions,
        min_support=min_support,
        min_confidence=min_confidence,
        min_lift=min_lift)
    rules = list(rules)

    to_rule_row = lambda item : AssociationRuleRow(
       antecedent=", ".join(list(item[2][0][0])),
       consequent=", ".join(list(item[2][0][1])),
       support=item[1],
       confidence=item[2][0][2],
       lift=item[2][0][3]
    )
    rules = list(map(to_rule_row ,rules))
    rules.sort()
    rules.reverse()

    return rules

