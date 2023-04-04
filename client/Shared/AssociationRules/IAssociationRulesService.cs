public interface IAssociationRulesService
{
  public Task<List<FileModel>> GetFiles();
  public Task<FileModel> RemoveFile(int fileId);
  public Task<FileContentModel> GetFileContent(int fileId);
  public Task<List<FrequencyAnalysisResponse>> GetFrequencies(int fileId);
  public Task<List<AssociationRulesResponse>> GetAssociationRules(int fileId, float minSupport, float minConfidence, float minLift);
  public string GetFileUrl(int fileId);
  public string GetAssociationRulesUrl(int fileId, float min_support, float min_confidence, float min_lift);
}