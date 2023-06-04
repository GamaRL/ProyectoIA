public interface ILogisticRegressionService
{
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  string GetImageUrl(string resource);
  Task<RegressionSettingsData> GetRegressionSettingsData(int fileId);
  Task SaveRegressionSettingsData(RegressionSettingsData settings);
  Task<RegressionInfoResponse> GetRegressionInfo(int fileId);
  Task<RegressionExecutionResponse> GetRegressionExecutionResponse(int fileId, Dictionary<string, float> register);
  Task<List<object>> GetValidClassVariables(int fileId);
}