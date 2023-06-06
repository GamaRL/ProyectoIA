public interface IPrognosisService
{
  Task<PrognosisSettingsData> GetSettingsData(int fileId);
  Task SaveSettingsData(PrognosisSettingsData settings);
  Task<PrognosisExecutionResponse> GetPrognosisExecutionResponse(int fileId, Dictionary<string, float> register);
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  string GetImageUrl(string resource);
}