using AdrGuardDemo.Domain;

namespace AdrGuardDemo.Infrastructure.Persistence;

public sealed class PostgresOrderRepository
{
    public Task SaveAsync(Order order, CancellationToken cancellationToken = default) =>
        Task.CompletedTask;
}
