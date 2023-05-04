import pandas as pd
from sqlalchemy.orm import Session
from apyori import apriori

from ..schemas import AssociationRuleExecResponse, AssociationRuleRow, StatisticsRow
from ..models import AssociationRule, AssociationRuleExec
from ..crud.file_service import __get_file_path__, get_file_by_id


def get_frequency_table_from_file(db: Session, file_id: int):
    file = get_file_by_id(db, file_id)
    path = __get_file_path__(file)
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
    file_path = __get_file_path__(file)

    content = pd.read_csv(file_path, header=None)

    transactions = content.stack().groupby(level=0).apply(list).tolist()
    rules = apriori(
        transactions=transactions,
        min_support=min_support,
        min_confidence=min_confidence,
        min_lift=min_lift)
    rules = list(rules)

    def to_rule_row(item): return AssociationRuleRow(
        antecedent=", ".join(list(item[2][0][0])),
        consequent=", ".join(list(item[2][0][1])),
        support=item[1],
        confidence=item[2][0][2],
        lift=item[2][0][3]
    )
    rules = list(map(to_rule_row, rules))
    rules.sort()
    rules.reverse()

    return rules

def save_rule_from_file(db: Session, file_id: int, rules: list[AssociationRuleRow]):
    file = get_file_by_id(db, file_id)

    exec_rule = AssociationRuleExec(
        file_id=file.id,
    )

    db.add(exec_rule)
    db.commit()
    db.refresh(exec_rule)

    for rule in rules:
        created_rule = AssociationRule(
            exec_id=exec_rule.id,
            antecedent=rule.antecedent,
            consequent=rule.consequent,
            support=rule.support,
            confidence=rule.confidence,
            lift=rule.lift
        )
        db.add(created_rule)
    db.commit()
    return exec_rule
    
def get_rule_from_file(db: Session, file_id: int):
    association_exec = db.query(AssociationRuleExec).filter(AssociationRuleExec.file_id == file_id).all()

    response = []

    for rule in association_exec:
        rules = db.query(AssociationRule).filter(AssociationRule.exec_id == rule.id).all()
        rules = list(map(lambda x: AssociationRuleRow(
            antecedent=x.antecedent,
            consequent=x.consequent,
            support=x.support,
            confidence=x.confidence,
            lift=x.lift
        ), rules))
        register = AssociationRuleExecResponse(
            id = rule.id,
            created_at = rule.created_at,
            rules = rules
        )
        response.append(register)

    return response

