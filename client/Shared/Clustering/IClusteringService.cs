public interface IClusteringService
{
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  Task<List<AgglomerativeClusterResponse>> GetAgglomerativeClusters(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric, bool download = false);
  string GetCorrelationUrl(CorrelationAnalysisResponse response);
}