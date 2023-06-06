public interface IClassificationService
{
  Task<ClassificationSettingsData> GetSettingsData(int fileId);
  Task SaveSettingsData(ClassificationSettingsData settings);
  Task<List<object>> GetValidClassVariables(int fileId);
  Task<ClassificationExecutionResponse> GetPrognosisExecutionResponse(int fileId, Dictionary<string, float> register);
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  // Task<PrognosisInfoResponse> GetPrognosisInfo(int fileId);
  string GetImageUrl(string resource);
}