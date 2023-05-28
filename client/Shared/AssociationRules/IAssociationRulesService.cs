public interface IAssociationRulesService
{
  public Task<List<FrequencyAnalysisResponse>> GetFrequencies(int fileId);
  public Task<List<AssociationRulesResponse>> GetAssociationRules(int fileId, float minSupport, float minConfidence, float minLift);
  public string GetAssociationRulesUrl(int fileId, float min_support, float min_confidence, float min_lift);
  public void SaveRules(int fileId, List<AssociationRulesResponse> rules);
  public Task<List<AssociationRulesExecResponse>> GetExecRules(int fileId);
}
