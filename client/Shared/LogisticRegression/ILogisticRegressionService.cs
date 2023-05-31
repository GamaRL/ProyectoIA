public interface ILogisticRegressionService
{
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  string GetImageUrl(string resource);
  Task<RegressionSettingsData> GetRegressionSettingsData(int fileId);
  Task SaveRegressionSettingsData(RegressionSettingsData settings);
}